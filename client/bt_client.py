#! python3 -m pip install -r requirements.txt
import socket
import math
import spidev
import board
import digitalio
from time import sleep
from adafruit_debouncer import Debouncer
import speech_recognition as sr

CENTER_X = 0
CENTER_Y = 523

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

# SETUP MICROPHONE FOR SPEECH TO TEXT
def setup_mic():
    global r
    r = sr.Recognizer()
    global speech
    speech = sr.Microphone(device_index=1)  

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

        # Begin recording for speech to text
        with speech as source:
            print("STARTING RECORDING...")
            audio = r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                transcribed_text = r.recognize_google(audio, language = "en-US")
                
                print("You said: " + transcribed_text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # Detect button released
    if ptt.rose:
        print("PTT Up")
        mic_stream = "s2t$" + transcribed_text

    # Send packet to host PC
    if mic_stream != "":
        s.send(mic_stream.encode())
        mic_stream = ""

############################################################
def ichi_client():
    setup_connection()
    setup_io()
    setup_mic()

    try:
        while True:
            button_listener(mb_l, "MBL")
            button_listener(mb_r, "MBR")
            # mb_m_listener()
            joystick_listener()           # TODO: Validate Continuous Sampling
            speech_to_text_handler()        # TODO: Validate only record on PTT push

    except KeyboardInterrupt:
        s.close()
        print('\n')

if __name__ == "__main__":
    ichi_client()