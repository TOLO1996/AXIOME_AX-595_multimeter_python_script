import signal
import sys
import time
import serial


class Multimeter:
    def __init__(self, interface, model, baudrate=2400):
        self.interface = interface
        self.baudrate = baudrate
        self.model = model
        self.port = None

    def connect(self):
        '''
        Try to connect to serial port 
        '''
        try:
            self.port = serial.Serial(
                self.interface,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                parity=serial.PARITY_NONE,
                timeout=5.0
            )
            if not self.port.isOpen():
                self.port.open()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def get_raw_data(self):
        '''
        Gets raw data from serial port, correct data is 112 bit long, sometimes this function returns 70 bit
        This behavior generates error so i check if data have 112 bit, to prevent from stucking in while 
        timeout is added
        '''
        start_time = time.time()  # Record the start time
        while True:
            data = self.port.read_until(b'\r\n')  # Read data until CR LF
            binary_data = ''.join(format(byte, '08b') for byte in data)
            #self.validate_binary_data(binary_data)
            # Check if the length of binary_data is 112
            if len(binary_data) == 112:
                self.port.flush()
                self.port.reset_input_buffer() #this is important!
                #print(binary_data)
                return binary_data
            else:
                # Check if timeout has been exceeded
                if time.time() - start_time > 10:
                    raise TimeoutError("Timeout exceeded while waiting for valid data.")
                print("Invalid data length! Expected 112 characters, got", len(binary_data))
                print("Attempting to read data again...")

    def signal_handler(self, signal, frame):
        sys.stderr.write('\n\nYou pressed Ctrl+C!\n\n')
        if self.port:
            self.port.flush()
            self.port.reset_input_buffer() 
            self.port.close()
        sys.exit(0)

    def stream_decode_new(self,substr):
        '''
        Data streamed drom multimeter are in following manner
        0-7 bit sign character "-" or ""
        8-40 are 4 digits write in 8 bit ASCII
        bits 53 to 55 are three dots beetwen digits where 1 means "." and 0 ""
        bit beetwen 88-96 contain value of the analogue Bar - and don not use this here it is save as "raw" binary with values from 0 to 60

        '''
        # Extract segments
        # Convert binary to ASCII
        sign_char_ascii = chr(int(substr[0:8], 2))
        sign_char_ascii = "" if sign_char_ascii != "-" else sign_char_ascii #check if this is "-"
        digit1_ascii = self.extract_ascii(substr, 8, 16)
        digit2_ascii = self.extract_ascii(substr, 16, 24)
        digit3_ascii = self.extract_ascii(substr, 24, 32)
        digit4_ascii = self.extract_ascii(substr, 32, 40)
        # Extract dots from imput string 
        dot1 = "." if substr[55] == "1" else ""
        dot2 = "." if substr[54] == "1" else ""
        dot3 = "." if substr[53] == "1" else ""
        # Merge digits and dots to form the final number
        final_number = (sign_char_ascii + digit1_ascii + dot1 + digit2_ascii + dot2 + digit3_ascii + dot3 + digit4_ascii)
        
        # Extract flags
        auto, dc, ac = int(substr[58]), int(substr[59]), int(substr[60])
        # Extract additional symbols
        symbols = {
            'micro': int(substr[72]), 'cap': int(substr[85]), 'nano': int(substr[70]),
            'diotst': int(substr[77]), 'lowbat': int(substr[69]), 'kilo': int(substr[74]),
            'mili': int(substr[73]), 'percent': int(substr[78]), 'mega': int(substr[75]),
            'contst': int(substr[76]), 'ohm': int(substr[82]),
            'hold': int(substr[62]), 'amp': int(substr[81]), 'volts': int(substr[80]),
            'hertz': int(substr[84]),'fahrenh': int(substr[87]),
            'celcius': int(substr[86])
        }

        # Construct flags and units strings
        flags = " ".join([name for name, present in {
            "AC": ac, "DC": dc, "Auto": auto, "Diode test": symbols['diotst'],
            "Conti test": symbols['contst'], "Capacity": symbols['cap'],
            "Hold": symbols['hold'], "LowBat": symbols['lowbat']
        }.items() if present])

        units = "".join([symbol for symbol, present in {
            "n": symbols['nano'], "u": symbols['micro'], "k": symbols['kilo'],
            "m": symbols['mili'], "M": symbols['mega'], "%": symbols['percent'],
            "Ohm": symbols['ohm'], "Amp": symbols['amp'], "Volt": symbols['volts'],
            "Hz": symbols['hertz'], "F": symbols['fahrenh'], "C": symbols['celcius']
        }.items() if present])

        return final_number +" "+ flags + " " + units
        #return value + " " + flags + " " + units

    def extract_ascii(self,substr, start, end):
        '''
        Conert part of binary string [star:end] to ASCII
        Usage:
        sign_char_ascii = extract_ascii(substr, 0, 8)
        digit1_ascii = extract_ascii(substr, 8, 16)
        '''
        try:
            return chr(int(substr[start:end], 2))
        except (ValueError, IndexError):
            return ""
        
    def validate_binary_data(self, binary_data):
        '''
        Check if input data is binary
        '''
        if all(char in "01" for char in binary_data):
            return True  # Data is valid
        else:
            print("Error: Binary data contains invalid characters.")
            return False  # Data is invalid
        


if __name__ == "__main__":
    meter1 = Multimeter("COM4", "AX-595")
    meter1.connect()

    # Set up the signal handler
    signal.signal(signal.SIGINT, meter1.signal_handler)
    
    try:
        while True:
            #input("Press Enter to continue...")
            result = meter1.get_raw_data()
            print(meter1.stream_decode_new(result))

    except KeyboardInterrupt:
        meter1.signal_handler(None, None)

