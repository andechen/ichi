# Hardware Report
## Hardware Pinout
| Raspberry Pi Pin # | Usage/Description |
| ------------ | -------|
| GPIO4 | Right push button input |
| GPIO22 | Left push button input |
| GPIO10 | Serial Data In for Analog-to-Digital Converter (ADC) for Joystick |
| GPIO9 |Serial Data Out for ADC |
| GPIO11 | Clock for ADC |
| GPIO6 | Push to Talk button input |
| GPIO8 | Chip Select/ Shut Down for ADC |
| 5V | 5V connection to battery pack |
| GND | Grounding connections for all components |
| 3V3 | 3.3V power for all components|

## Controller 
### Bill of Materials
| Component | Quantity | Vendor | Total Cost | 
| ------------ | -------| -------| -------|
| Tobii Eye Tracker 5 | 1 | Tobii | $220.15 |
| Raspberry Pi Zero 2W | 1 | Amazon | $89.90 |
| PiSugar 1200 mAh Battery Module | 1 | Amazon | $38.99 |
| MCP3008 8-Channel 10-Bit ADC | 1 | Adafruit | $9.00 |
| Analog 2-Axis Joystick | 1 | Digikey | $4.50 |
| Joystick Breakout Board | 1 | Digikey | $2.10 |
| Protoboard | 1 | Digikey | $4.50 |
| Mini USB Microphone | 1 | Digikey | $5.95 |
| Tactile Switch Buttons | 3 | Digikey | $0.69 |
| 3D Printed Controller Shell | 1 | N/A | N/A |
| | | | $375.78 |

### Circuit Diagram
![circuit](https://user-images.githubusercontent.com/60196943/235364928-e4cb3a6f-1d31-42ff-a8e2-0e9d899382b8.png)

### Controller Image
![controller](https://user-images.githubusercontent.com/60196943/235365123-d277ea2b-d3c5-401a-89c5-5e07fab8c438.png)
![Wiring](https://user-images.githubusercontent.com/60196943/235370242-beb087c2-de2b-4e12-a860-c6ff7ec91cbc.jpeg)

### CAD Diagrams of 3D printed controller
The CAD files used to print the controller are located in the CAD files folder. 
Large Button 
![Large_Button_Drawing](https://user-images.githubusercontent.com/60196943/235370122-159330f7-593d-4b48-806c-62ace187ebf5.jpg)
Small Button
![Small_Button_Drawing](https://user-images.githubusercontent.com/60196943/235370125-70b38b81-3b8c-4dcd-a0ea-9d57cbc522e1.jpg)
Top View
![Top_Drawing](https://user-images.githubusercontent.com/60196943/235370128-27b56ca2-2e74-4766-bbee-b6bf2f8c92ff.jpg)
Bottom View
![Bottom_Drawing](https://user-images.githubusercontent.com/60196943/235370114-ee1d3a53-a749-4566-94e3-a49d80ad8314.jpg)

## Tobii Eye Tracker
To set up the Tobii Eye Tracker 5, the driver software, Tobii Experience Software for Windows, must be installed. 
The eye tracker must be mounted on the screen it will be used on. Once the device is plugged in via USB, the eye tracker is ready to go. 
