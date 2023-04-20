import serial
import pyautogui

# TODO: 
#   handle interruptions to socket
#   cursor movement

# s = serial.Serial('COM3')
s = serial.Serial('COM4')

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
                pyautogui.click(button='middle')
        case 's2t':
            pyautogui.write("t")
            pyautogui.write(pkt_array[-1])
        case 'SCRL':
            x_delta = int(pkt_array[1])
            y_delta = int(pkt_array[2])
            print("X: " + str(x_delta) + " | Y: " + str(y_delta))
            pyautogui.scroll(y_delta // 2)
        case 't':
            pyautogui.write('t')

def ichi_host():
    while True:
        rec = s.readline()
        recvd_packet = rec.decode()

        split_pkt = recvd_packet.split("$")
        parse_packet(split_pkt)

if __name__ == "__main__":
    ichi_host()