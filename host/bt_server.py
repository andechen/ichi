import serial

s = serial.Serial('COM4')

# while True:
res = s.read()
print(res)