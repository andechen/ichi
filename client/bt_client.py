import socket
from time import sleep

# Device specific information
bd_addr = "7C:50:79:3E:8F:2C"
port = 4 # This needs to match M5Stick setting

# Establish connection and setup serial communication
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((bd_addr, port))

# Send and receive data
while True:
    s.sendall(b'X\n')
    data = s.recv(1024)
    print(data)
    sleep(0.5)
s.close()

# bd_addr = "7C:50:79:3E:8F:2C"

# port = 1

# sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
# sock.connect((bd_addr, port))

# sock.send("Hello World!")

# sock.close()