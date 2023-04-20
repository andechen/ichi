#! python3 -m pip install -r requirements.txt
from __future__ import division
import socket
import math
import spidev
import board
import digitalio
from time import sleep
from adafruit_debouncer import Debouncer
import re
import sys
import os
from google.cloud import speech
import pyaudio
from six.moves import queue

# Joystick noise dampening parameters
CENTER_X = 0
CENTER_Y = 523

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# LED is pin 26

################## SPEECH TO TEXT CLASSES ##################
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

##################### HELPER FUNCTIONS #####################
# SETUP BLUETOOTH SOCKET
def setup_connection():
    # ANDE LAPTOP MAC ADDR: 7C:50:79:3E:8F:2C
    # ANDE LAPTOP PORT: 4
    # LAB DESKTOP MAC ADDR: A0:36:BC:DA:1B:68
    # LAB DESKTOP PORT: 3
    # host_addr = "A0:36:BC:DA:1B:68"     # Host PC's MAC address
    # port = 3                            # Connect to port on Host PC
    host_addr = "7C:50:79:3E:8F:2C"     # Host PC's MAC address
    port = 4                            # Connect to port on Host PC

    # SET UP CONNECTION
    global s
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((host_addr, port))
    print("CONNECTION ESTABLISHED WITH " + host_addr + " PORT " + str(port))

# SETUP GPIO PINS AND DEBOUNCING
def setup_io():
    # LEFT CLICK BUTTON
    pin_MB_L = digitalio.DigitalInOut(board.D22)
    pin_MB_L.direction = digitalio.Direction.INPUT
    pin_MB_L.pull = digitalio.Pull.UP
    global mb_l
    mb_l = Debouncer(pin_MB_L)

    # RIGHT CLICK BUTTON
    pin_MB_R = digitalio.DigitalInOut(board.D4)
    pin_MB_R.direction = digitalio.Direction.INPUT
    pin_MB_R.pull = digitalio.Pull.UP
    global mb_r
    mb_r = Debouncer(pin_MB_R)

    # PUSH TO TALK BUTTON
    pin_PTT = digitalio.DigitalInOut(board.D5)
    pin_PTT.direction = digitalio.Direction.INPUT
    pin_PTT.pull = digitalio.Pull.UP
    global ptt
    ptt = Debouncer(pin_PTT)

    # SPI BUS FOR JOYSTICK
    global swt_channel
    global x_channel
    global y_channel

    swt_channel = 0
    x_channel = 1
    y_channel = 2

    global spi
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000

# SETUP MICROPHONE
def setup_mic():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "en-US"  # a BCP-47 language tag

    global client
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    global streaming_config
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

# LISTEN FOR BUTTON PRESS AND RELEASE
def button_listener(button_obj, button_name):
    data_stream = ""
    button_obj.update()

    # Detect button pressed
    if button_obj.fell:
        print(button_name + " Down")
        data_stream = button_name + "$1\n"

    # Detect button released
    if button_obj.rose:
        print(button_name + " Up")
        data_stream = button_name + "$0\n"

    # Send packet to host PC
    if data_stream != "":
        s.send(data_stream.encode())
        data_stream = ""

# JOYSTICK HELPER FUNCTIONS
def read_spi_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

def joystick_listener():
    x_delta = read_spi_channel(x_channel) - CENTER_X
    y_delta = read_spi_channel(y_channel) - CENTER_Y

    if ((y_delta <= -25) or (y_delta >= 25)):
        data_stream = "SCRL$" + str(x_delta) + "$" + str(y_delta) + "\n"
        print("VRx : {}  VRy : {}".format(x_delta, y_delta))
        sleep(0.07)
        s.send(data_stream.encode())
        data_stream = ""

def mb_m_listener():
    prev_state = 1
    curr_state = 0
    toggled = False
    mb_m = read_spi_channel(swt_channel)

    if mb_m == 1:
        if prev_state != curr_state:
            curr_state = 1
            sleep(0.5)
        else:
            curr_state = 0
            sleep(0.5)
        print("MBM Down")
        data_stream = "MBM$1\n"
        s.send(data_stream.encode())
        data_stream = ""

# SPEECH TO TEXT HANDLER
def speech_to_text_handler():
    mic_stream = ""
    ptt.update()

    # Detect button pressed
    if ptt.fell:
        print("PTT Down")
        s.send("t".encode())

        # Begin recording for speech to text
        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config, requests)

            num_chars_printed = 0

            for response in responses:
                if not response.results:
                    continue

                result = response.results[0]
                if not result.alternatives:
                    continue

                # Display the transcription of the top alternative.
                transcript = result.alternatives[0].transcript

                overwrite_chars = " " * (num_chars_printed - len(transcript))

                if not result.is_final:
                    sys.stdout.write(transcript + overwrite_chars + "\r")
                    sys.stdout.flush()

                    num_chars_printed = len(transcript)

                else:
                    print(transcript + overwrite_chars)
                    mic_stream = "s2t$" + transcript + overwrite_chars

                    num_chars_printed = 0

    # Detect button released
    if ptt.rose:
        print("PTT Up")

        # Send packet to host PC
        if mic_stream != "" and mic_stream != "s2t$":
            s.send(mic_stream.encode())
            mic_stream = ""

############################################################
def ichi_client():
    setup_connection()
    setup_io()
    setup_mic()

    try:
        while True:
            #button_listener(mb_l, "MBL")
            #button_listener(mb_r, "MBR")
            # mb_m_listener()
            #joystick_listener()           # TODO: Validate Continuous Sampling
            speech_to_text_handler()        # TODO: Validate only record on PTT push

    except KeyboardInterrupt:
        s.close()
        print('\n')

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cybernetic-hue-384302-2e9e296cbd96.json'
    ichi_client()