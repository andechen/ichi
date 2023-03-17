#! python3 -m pip install -r requirements.txt
import socket
import board
import digitalio
from adafruit_debouncer import Debouncer

##################### HELPER FUNCTIONS #####################
# SETUP BLUETOOTH SOCKET
def setup_connection():
    host_addr = "7C:50:79:3E:8F:2C"     # Host PC's MAC address
    port = 4                            # Connect to COM4

    # SET UP CONNECTION
    global s
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((host_addr, port))
    print("CONNECTION ESTABLISHED WITH " + host_addr + " PORT " + str(port))

# SETUP GPIO PINS AND DEBOUNCING
def setup_gpio():
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
    pin_MB_M = digitalio.DigitalInOut(board.D4)     #TODO: Update joystick select pin number
    pin_MB_M.direction = digitalio.Direction.INPUT
    pin_MB_M.pull = digitalio.Pull.UP
    global mb_m
    mb_m = Debouncer(pin_MB_M)

    # PUSH TO TALK BUTTON
    pin_PTT = digitalio.DigitalInOut(board.D23)
    pin_PTT.direction = digitalio.Direction.INPUT
    pin_PTT.pull = digitalio.Pull.UP
    global ptt
    ptt = Debouncer(pin_PTT)

# LISTEN FOR BUTTON PRESS AND RELEASE
def button_listener(button_obj, button_name):
    button_stream = ""

    # while True:
    button_obj.update()

    if button_obj.fell:
        print(button_name + " Down")
        button_stream = button_name + "$1\n"
    if button_obj.rose:
        print(button_name + " Up")
        button_stream = button_name + "$0\n"

    if button_stream != "":
        s.send(button_stream.encode())
        button_stream = ""

############################################################
def ichi_client():
    setup_connection()
    setup_gpio()

    try:
        while True:
            button_listener(mb_l, "MBL")
            button_listener(mb_r, "MBR")
            button_listener(ptt, "PTT")

    except KeyboardInterrupt:
        s.close()
        print('\n')

if "__name__" == "__main__":
    ichi_client()