from multiprocessing import Process
import sounddevice as sd
import pyaudio
from mic import *
# from mouse import *

if __name__ =="__main__":
    # Detect microphone as input device
    #print(sd.query_devices())

    #p = pyaudio.PyAudio()
    #for ii in range(p.get_device_count()):
    #    print(p.get_device_info_by_index(ii).get('name'), "Input Device id ", ii)

    # Create thread for speech transcription
    #speech_to_text = Process(target = transcribe, args=())

    # Create thread for mouse button inputs
    # t2 = threading.Thread(target = print_cube, args=(10,))

    # Start threads
    #speech_to_text.start()
    # t2.start()

    #speech_to_text.join()
