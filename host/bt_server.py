#! python3 -m pip install -r requirements.txt
import serial
import pyautogui
import sys

# TODO: 
#   joystick code
#   handle interruptions to socket
#   cursor movement

s = serial.Serial('COM4')

screen_res = pyautogui.size()
MIN_X = 1
MIN_Y = 1
MAX_X = screen_res[0]
MAX_Y = screen_res[1]

def parse_packet(pkt_array):
    pkt_array[-1] = pkt_array[-1].replace('\n','')
    print(pkt_array)

    match pkt_array[0]:
        case 'MBL':
            if pkt_array[1] == '1':
                pyautogui.mouseDown(button='left')
            elif pkt_array[1] == '0':
                 pyautogui.mouseUp(button='left')
        case 'MBR':
            if pkt_array[1] == '1':
                pyautogui.mouseDown(button='right')
            elif pkt_array[1] == '0':
                 pyautogui.mouseUp(button='right')
        case 'MBM':
            if pkt_array[1] == '1':
                pyautogui.mouseDown(button='middle')
            elif pkt_array[1] == '0':
                 pyautogui.mouseUp(button='middle')
        case 's2t':
            pyautogui.write(pkt_array[-1])

# def tobii_handler(gazepoint_x, gazepoint_y):
#     # Position mouse cursor to user gazepoint
#     pyautogui.moveTo(gazepoint_x, gazepoint_y)
#     # TODO: don't move cursor off screen
#     if (gazepoint_x > MAX_X):
#         gazepoint_x = gazepoint_x - 1
#     if (gazepoint_y) > MAX_Y:
#         gazepoint_y = gazepoint_y - 1

while True:
    rec = s.readline()
    recvd_packet = rec.decode()

    split_pkt = recvd_packet.split("$")
    parse_packet(split_pkt)