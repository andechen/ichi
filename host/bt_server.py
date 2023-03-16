import serial

s = serial.Serial('COM4')
res = s.read()
print(res)