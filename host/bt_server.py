import serial

s = serial.Serial('COM4')

# while True:
res = s.readline()
print(res)