import sys
import RPi.GPIO as GPIO
import pyautogui



print('Press Ctrl-C to quit.')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
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