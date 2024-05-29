## Import the required package
import serial
from datetime import datetime
import json
from paho.mqtt import client as mqtt_client
import random

## Setup the LoRa Arduino receiver
arduino_port = '/dev/ttyUSB0'
arduino_baudrate = 9600

## Setup the MQTT connection to the cloud server
server = "<your server IP>"
port = <your server port>
topic = "Sensors/Environment/LoRa"
client_id = f'edge-{random.randint(0,100)}'

t = int(datetime.now().strftime('%H%M%S'))

def connect_server():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Server")
        else:
            print("Failed to connect to Server")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(server, port)
    return client

def send_to_server(edge_client, data):
    tstamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    send_data = {
        "Timestamp": tstamp,
        "Device_ID": data[1],
        "Humidity": data[3:7],
        "Temperature": data[8:]
    }
    send_data = json.dumps(send_data)
    result = edge_client.publish(topic, send_data)
    if result[0] == 0:
        print("{} Success send data to server".format(tstamp))

if __name__ == '__main__':
    ## Connect to the LoRa Arduino receiver
    serial_conn = serial.Serial(arduino_port, arduino_baudrate)
    serial_conn.reset_input_buffer()
    
    ## Connect to the cloud server
    edge_client = connect_server()
    
    print("Start Collecting data from the LoRa receiver")
    while serial_conn.is_open:
        if serial_conn.in_waiting > 0:
            try:
                data = serial_conn.readline().decode("utf-8").rstrip()

                if len(data) > 1:
                    send_to_server(edge_client, data)
                    
                    ## Do any other required task here
                    ## Save to edge database
                    ## Visualization
                    ## AI inference
                
            except:
                print('No data received or error when sending data')
        
