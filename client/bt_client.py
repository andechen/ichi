import serial

ser = serial.Serial('COM4')
print(ser.name)
ser.write('Hello World')
ser.close()
print("Closed Socket")

# bd_addr = "7C:50:79:3E:8F:2C"