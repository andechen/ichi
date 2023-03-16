import serial

s = serial.Serial('COM4')

try:
    while True:
        res = s.readline()
        res.decode()
        print(res)
except KeyboardInterrupt:
    print('\n')