import serial

s = serial.Serial('COM4')

try:
    while True:
        res = s.readline()
        print(res)
except KeyboardInterrupt:
    print('\n')