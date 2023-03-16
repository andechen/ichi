#! python3 -m pip install -r requirements.txt
import socket
import board
import digitalio
from adafruit_debouncer import Debouncer
from multiprocessing import Process

#################### PROCESS TASKS ####################
def button_listener(button_obj, button_name):
    button_stream = ""

    # while True:
    button_obj.update()

    if button_obj.fell:
        print(button_name + " Down")
        button_stream = button_name + "$1\n"
    if button_obj.rose:
        print(button_name + " Release")
        button_stream = button_name + "$0\n"

    if button_stream != "":
        s.send(button_stream.encode())
        button_stream = ""

#################### HOST DEVICE INFORMATION ####################
host_addr = "7C:50:79:3E:8F:2C"     # Host PC's MAC address
port = 4                            # Connect to COM4

# SET UP CONNECTION
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((host_addr, port))
print("CONNECTION ESTABLISHED WITH " + host_addr + " PORT " + str(port))

#################### SETUP GPIO PINS ####################
# LEFT CLICK BUTTON
pin_MB_L = digitalio.DigitalInOut(board.D22)
pin_MB_L.direction = digitalio.Direction.INPUT
pin_MB_L.pull = digitalio.Pull.UP
mb_l = Debouncer(pin_MB_L)

# RIGHT CLICK BUTTON
pin_MB_R = digitalio.DigitalInOut(board.D4)
pin_MB_R.direction = digitalio.Direction.INPUT
pin_MB_R.pull = digitalio.Pull.UP
mb_r = Debouncer(pin_MB_R)

# MIDDLE CLICK BUTTON
pin_MB_M = digitalio.DigitalInOut(board.D4)     #TODO: Update joystick select pin number
pin_MB_M.direction = digitalio.Direction.INPUT
pin_MB_M.pull = digitalio.Pull.UP
mb_m = Debouncer(pin_MB_M)

# PUSH TO TALK BUTTON
pin_PTT = digitalio.DigitalInOut(board.D23)
pin_PTT.direction = digitalio.Direction.INPUT
pin_PTT.pull = digitalio.Pull.UP
ptt = Debouncer(pin_PTT)

#################### SETUP MULTI-PROCESSING ####################
processlist = []
processlist.append(Process(target=button_listener(mb_l, "MBL")))
processlist.append(Process(target=button_listener(mb_r, "MBR")))
processlist.append(Process(target=button_listener(ptt, "PTT")))

# Send data
try:
    while True:
        # button_listener(mb_l, "MBL")
        for p in processlist:
            p.start()

        # for p in processlist:
        #     p.join()

except KeyboardInterrupt:
    s.close()
    print('\n')