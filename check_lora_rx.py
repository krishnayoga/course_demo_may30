## Import the required package
import serial

## Setup the LoRa Arduino receiver
arduino_port = '/dev/ttyUSB0'
arduino_baudrate = 9600

if __name__ == '__main__':
    ## Connect to the LoRa Arduino receiver
    serial_conn = serial.Serial(arduino_port, arduino_baudrate)
    serial_conn.reset_input_buffer()
    
    print("Start Collecting data from the LoRa receiver")
    while serial_conn.is_open:
        if serial_conn.in_waiting > 0:
            try:
                data = serial_conn.readline().decode("utf-8").rstrip()

                if len(data) > 1:
                    print('Retrieved data', data)
                    
                    ## Do any other required task here
                    ## Save to edge database
                    ## Visualization
                    ## AI inference
                
            except:
                print('No data received or error when sending data')
        
