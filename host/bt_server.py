#! python3 -m pip install -r requirements.txt
import serial
import pyautogui

s = serial.Serial('COM4')

def parse_packet(pkt_array):
    print(pkt_array)

    match pkt_array[0]:
        case "MBL":
            if pkt_array[1] == "1":
                pyautogui.mouseDown(button='left')
            elif pkt_array[1] == "0":
                 pyautogui.mouseUp(button='left')
        case "MBR":
            if pkt_array[1] == "1":
                pyautogui.mouseDown(button='right')
            elif pkt_array[1] == "0":
                 pyautogui.mouseUp(button='right')
        case "MBM":
            if pkt_array[1] == "1":
                pyautogui.mouseDown(button='middle')
            elif pkt_array[1] == "0":
                 pyautogui.mouseUp(button='middle')
        case "PTT":
            print("PTT")

while True:
    rec = s.readline()
    recvd_packet = rec.decode()

    split_pkt = recvd_packet.split("$")
    parse_packet(split_pkt)