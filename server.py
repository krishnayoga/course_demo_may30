from paho.mqtt import client as mqtt_client
import random
import mariadb
import json

## Setup the MQTT in cloud server
server = "<your server IP>"
port = <your server port>
topic = "Sensors/Environment/LoRa"
client_id = f'server-{random.randint(0,100)}'

def connect_mqtt_server() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Server")
        else:
            print("Failed to connect tp server")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(server, port)
    return client

def subscribe_to_topic(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        jsonData = json.loads(msg.payload.decode())
        timestamp = jsonData['Timestamp']
        device_id = jsonData['Device_ID']
        humidity = jsonData['Humidity']
        temperature = jsonData['Temperature']
        db_conn = mariadb.connect(host="<your DB server IP>", user="<your DB server username>", password="<your DB server password>", database="<your DB server DB name>", port=<your DB server port>) #Depends on the DB config
        db_cursor = db_conn.cursor()
        db_command1 = f"INSERT INTO `lora_sensors` (`Device_ID`, `Humidity`, `Temperature`) VALUES ({device_id},{humidity},{temperature})" #Depends on the DB table
        db_cursor.execute(db_command1)
        db_conn.commit()
        db_cursor.close()
        db_conn.close()    

    client.subscribe(topic)
    client.on_message = on_message

if __name__ == '__main__':
    client = connect_mqtt_server()
    subscribe_to_topic(client)
    client.loop_forever()
