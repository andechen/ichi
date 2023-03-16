import socket
import time
import board
import digitalio
from adafruit_debouncer import Debouncer
from multiprocessing import Process

#! python3 -m pip install -r requirements.txt

# HOST DEVICE INFORMATION
host_addr = "7C:50:79:3E:8F:2C"     # Host PC's MAC address
port = 4                            # Connect to COM4

# SET UP CONNECTION
# s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# s.connect((host_addr, port))
# print("CONNECTION ESTABLISHED WITH " + host_addr + " PORT " + port + "...")

# SETUP GPIO PINS
pin_MB_L = digitalio.DigitalInOut(board.D22)
pin_MB_L.direction = digitalio.Direction.INPUT
pin_MB_L.pull = digitalio.Pull.UP
mb_l = Debouncer(pin_MB_L)

pin_MB_R = digitalio.DigitalInOut(board.D4)
pin_MB_R.direction = digitalio.Direction.INPUT
pin_MB_R.pull = digitalio.Pull.UP
mb_r = Debouncer(pin_MB_R)

# PROCESS TASKS
def button_listener(button):
    while True:
        button.update()

        # if button.fell:
        #     time_down = time.time()
        if button.rose:
            # time_up = time.time() - time_down
            # if time_up - time_down > 0.5:
            print("Click")

# SETUP MULTI-PROCESSING
# processlist = []
# processlist.append(Process(target=button_listener(mb_l)))
# processlist.append(Process(target=button_listener(mb_r)))
# 
# for p in processlist:
#     p.start()
# 
# for p in processlist:
#     p.join()

# Send data
try:
    while True:
        button_listener(mb_l)

        # data = "\n"
        # s.send(data.encode())

except KeyboardInterrupt:
    s.close()
    print('\n')