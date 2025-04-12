# AXIOME_AX-595_multimeter_python_script
Simple Python script to read data from AXIOME AXIOME_AX-595 multimeter
## Introduction
The purpose of this software is to be able to log data from the meter or meters connected to the computer's serial port using the Python language. The program is very simple and should be treated as a base for further expansion, in accordance with the individual project requirements.
A similar meter and method is described here:
https://alexkaltsas.wordpress.com/2013/04/19/python-script-to-read-data-from-va18b-multimeter/
And also on my github

## Description of operation
The program reads data from the serial port via an mini USB cable. Communication is one-way, multimeter -> computer, and it is not possible to change the meter's operating parameters from the computer.(At least that's what it looks like)
The documentation included on the disc is probably a mistake, but I haven't found a way to control the meter (which is what I was counting on!)
The biggest problem turned out to be decoding the data sent by the meter. Since this may be a hint for the future, they may help you connect other meters of this type, I will try to describe the entire process in quite detail.
### Step 1 Connect multimeter and install Drivers
This step is quite simple for this particular meter the drivers are included on the board. The system uses the CH340 converter and it will be visible in the device manager under this name.
I have attached the contents of the disc to this repository, you will find the appropriate driver there.

### Step 2 Get proper Boudrate
This step may be a bit difficult, you need to determine the speed at which data is exchanged. It turned out that the device uses the same speed as AXIOME_AX-18B, i.e. 2400
### Step 3 Listen to the protocol
Once we have determined the baud rate, we can run the serial port monitor, e.g. putty, set the appropriate parameters and try to read data from the port. 
#### Remember to turn on transmission on the meter, it is turned off by default. The operation of the transmission is signaled on the screen!
Then we set the meter to measure voltage and connect its measurement inputs. This way the meter will output a stable 0V reading. It is important that at this stage the meter constantly sends the same data.
In order to find the length of the frame sent by the meter, it is a good idea to set the data display method as single bits. And then determine the length of the repeating string.
![Binary](https://github.com/user-attachments/assets/c61db35b-a496-47d1-96f2-76b6a8ab4db5)
For this meter, the frame is 14 bytes
### Step 4 Data conversion
Once we know the frame length, we can start decoding individual bits. 
To make photo of all avaliable symbols, make the foto right after you turn on the device!
Data in this meter are sent in such a way that the symbol and the digit sign are sent in ASCII format, individual fields, e.g. AC, DC, etc. are sent as single bits, while the analog bar displayed at the bottom is displayed as a number from 0 to 63 (8 bits). The decoded symbols are shown in the image below
![Display_characters](https://github.com/user-attachments/assets/5506c825-8343-4963-b068-21c54f0cac75)

## Connecting the device
### Configuration

### Conections


## Mistakes and ideas for the future
