import sys
import RPi.GPIO as GPIO
import time
import serial
#import pyautogui

MB_R = 4
MB_L = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MB_R, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)      # R_MB
GPIO.setup(MB_L, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     # L_MB

ser = serial.Serial(
        port = '/dev/COM4', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout=1
)

counter = 0

print('Press Ctrl-C to quit.')
try:
    while True:
        # x, y = pyautogui.position()
        # positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        if GPIO.input(MB_R) == GPIO.HIGH:
            print("Right Click")

        if GPIO.input(MB_L) == GPIO.HIGH:
            print("Left Click")
        # print(positionStr, end='')
        # print('\b' * len(positionStr), end='', flush=True)

        # if keyboard.is_pressed('q'):
        #     pyautogui.click()
        #     print("Left Click at", positionStr)
        # elif keyboard.is_pressed('w'):
        #     pyautogui.click(button="right")
        #     print("Right Click at", positionStr)
        # elif keyboard.is_pressed('o'):
        #     pyautogui.press('home')
        # elif keyboard.is_pressed('p'):
        #     pyautogui.press('end')

        # Calculate delta from resting as greater magnitude of "clicks" to scroll

except KeyboardInterrupt:
    print('\n')