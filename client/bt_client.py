import bluetooth

bd_addr = "7C:50:79:3E:8F:2C"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("Hello World!")

sock.close()