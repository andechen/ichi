# Software Report
## Unity
The Unity Code is located in the folder named Unity Scripts. They contain the code for the game set up, the game manager code, and the game objects. In the Unity Executable folder > x64, there are files related to runnning the Unity executable. The ICHI Gaze.exe is the file needed to run the project. 
## Bluetooth
To properly establish Bluetooth connection between the controller and the host PC, first set up a COM port on the host PC to recieve Bluetoooth communications through the PC's Bluetooth settings. From the "Bluetooth & other devices" settings page go to "More Bluetooth options." Under the "COM Ports" tab, click Add. Leave the options as "Incoming (device initiates the connection)" and click OK. Note the COM port number that has been designated. In the bt_client.py script (/ichi/client), edit the host_addr variable to be the host PC's MAC address and the port to be the aforementioned COM port. Now, when the controller is plugged in, it will bind and connect to the host PC.
## Embedded Software
The Python script running on the Raspberry Pi within the controller should begin execution as soon as the Raspberry Pi recieves power.
## Controller Driver
The controller driver running on the host PC can be executed by simply running the "py bt_server.py" command in the command line.
