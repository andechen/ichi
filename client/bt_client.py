#! python3 -m pip install -r requirements.txt
import socket
import math
import spidev
import board
import digitalio
from adafruit_debouncer import Debouncer
import speech_recognition as sr

CENTER_X = 530
CENTER_Y = 504

##################### HELPER FUNCTIONS #####################
# SETUP BLUETOOTH SOCKET
def setup_connection():
    # ANDE LAPTOP MAC ADDR: 7C:50:79:3E:8F:2C
    # ANDE LAPTOP PORT: 4
    # LAB DESKTOP MAC ADDR: A0:36:BC:DA:1B:68
    # LAB DESKTOP PORT: 3
    host_addr = "A0:36:BC:DA:1B:68"     # Host PC's MAC address
    port = 3                            # Connect to port on Host PC

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

    # MIDDLE CLICK BUTTON
    # pin_MB_M = digitalio.DigitalInOut(board.D4)     #TODO: Update joystick select pin number
    # pin_MB_M.direction = digitalio.Direction.INPUT
    # pin_MB_M.pull = digitalio.Pull.UP
    # global mb_m
    # mb_m = Debouncer(pin_MB_M)

    # PUSH TO TALK BUTTON
    pin_PTT = digitalio.DigitalInOut(board.D23)
    pin_PTT.direction = digitalio.Direction.INPUT
    pin_PTT.pull = digitalio.Pull.UP
    global ptt
    ptt = Debouncer(pin_PTT)

    # TODO: SPI BUS FOR JOYSTICK
    # spi = spidev.SpiDev()
    # spi.open(0, 0)

    # x_channel = 1
    # y_chanenl = 2

# SETUP MICROPHONE FOR SPEECH TO TEXT
def setup_mic():
    global r
    r = sr.Recognizer()
    global speech
    speech = sr.Microphone(device_index=1)  

# LISTEN FOR BUTTON PRESS AND RELEASE
def button_listener(button_obj, button_name):
    button_stream = ""
    button_obj.update()

    # Detect button pressed
    if button_obj.fell:
        print(button_name + " Down")
        if button_name == 'PTT':
            speech_to_text_handler()
        else:
            button_stream = button_name + "$1\n"

    # Detect button released
    if button_obj.rose:
        print(button_name + " Up")
        button_stream = button_name + "$0\n"

    # Send packet to host PC
    if button_stream != "":
        s.send(button_stream.encode())
        button_stream = ""

# JOYSTICK HELPER FUNCTIONS
"""
def read_spi_data_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

def dampen_resting_pos(axis_val, centered_val):
    d = math.fabs(axis_val - centered_val)
    return d < 20

#TODO:
def joystick_listener(x_channel, y_channel):
    x_pos = read_spi_data_channel(x_channel)
    y_pos = read_spi_data_channel(y_channel)
    # TODO: convert change in pos to number of clicks
"""

# SPEECH TO TEXT HANDLER
def speech_to_text_handler():
    mic_stream = ""

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

    #     mic_stream = "s2t$" + transcribed_text

    # # Send packet to host PC
    # if mic_stream != "":
    #     s.send(mic_stream.encode())
    #     mic_stream = ""

############################################################
def ichi_client():
    setup_connection()
    setup_io()
    setup_mic()

    try:
        while True:
            button_listener(mb_l, "MBL")
            button_listener(mb_r, "MBR")
            button_listener(ptt, "PTT")
            speech_to_text_handler()

    except KeyboardInterrupt:
        s.close()
        print('\n')

if __name__ == "__main__":
    ichi_client()