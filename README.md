IoT Santa Claus
=======

## Santa Claus automation for my niece by face recognition
During a visit to the U.S. over Christmas to see a friend, we embarked on a delightful project to bring joy to his daughter. We automated a life-sized Santa Claus in his living room, complete with facial recognition, creating a magical and unforgettable experience.

### Video
[![IoT Santa Claus](https://img.youtube.com/vi/jBM-frhHqko/0.jpg)](https://youtu.be/jBM-frhHqko?si=ux92rnXBP_t_6cFA)

### Diagram
![oT Santa Claus](images/iot_santa_claus.drawio.png)

### Blog
[Santa Claus goes IoT](https://www.tweaklogic.com/santa-claus-goes-iot/)

### Prerequisites
1. PC/Laptop with network connection
OR
2. Raspberry Pi with monitor or touchscreen display (assuming default user **pi**)
3. TAPO Wi-Fi Smart plug: https://www.tapo.com/au/product/smart-plug/
4. Webcam

### TAPO Smart Plug

TP-Link TAPO Smart plugs are available off the shelf in Australia at Bunnings and Best Buy in the USA.
1. Install the TAPO app on your smartphone
2. Create user account and note down the credentials
3. Make sure you can operate the Smart Plug from your smartphone
4. Optionally go to device setting on your TAPO app and note down the IP address of the Smart Plug  


### Software Installation
1. Standard Ubuntu installation on any laptop or PC. Tested on Ubuntu 24.04.1 LTS
2. Raspberry Pi OS for Raspberry Pi. Tested on Bookworm 64 bit.
3. Clone this repository on your Raspberry Pi.
```
git clone 
```
4. Install the dependencies (dlib installation will take nearly an hour):
```
```
5. Copy the desktop shortcuts to ~/Desktop
6. Right click on the desktop shortcuts and make them executable.

### Operation

#### Training faces
1. Double click the **Santa Capture** icon
OR
2. Execute the below command from terminal
```
```
#### Starting the program
1. Double click the **OpenCV Santa** icon
OR
2. Execute the below command form terminal
```
```
#### Exiting the program
1. Mouse click and release on the screen or touch and release on a touchscreen
OR
2. Ctrl-C from terminal

#### TODO
Do a C++ implementation to make the code faster.
Support more IoT home automation devices.
