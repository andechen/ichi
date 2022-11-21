from machine import Pin, ADC
import time
import utime
led = Pin(25, Pin.OUT)

xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))
joystickButton = Pin(16,Pin.IN, Pin.PULL_UP)


left_button = Pin(21, Pin.IN, Pin.PULL_DOWN)
right_button = Pin(20, Pin.IN, Pin.PULL_DOWN)

while True:
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValue = joystickButton.value()

    print(str(xValue) +", " + str(yValue) + " -- " + str(buttonValue))
    time.sleep(0.2)
    if left_button.value():
        led.toggle()
        print("left button pressed")
        time.sleep(0.2)
    if right_button.value():
        print("right button pressed")
        time.sleep(0.2)
