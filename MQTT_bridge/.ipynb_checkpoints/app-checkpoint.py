import paho.mqtt.client as mqtt
import logging
import os
import json
import xml.etree.ElementTree as ET
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# Logging-Konfiguration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Umgebungsvariablen
mqtt_broker_host = os.getenv("MQTT_BROKER_HOST", "172.21.0.2")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT", "1883"))
mqtt_topic = os.getenv("MQTT_TOPIC", "AWS11")

# InfluxDB-Verbindungseinstellungen
influxdb_host = os.getenv("INFLUXDB_HOST", "172.21.0.4")
influxdb_port = int(os.getenv("INFLUXDB_PORT", "8086"))
influxdb_token = os.getenv("INFLUXDB_TOKEN")
influxdb_org = os.getenv("INFLUXDB_ORG","meineOrganisation")  # Stellen Sie sicher, dass diese Zeile korrekt ist
influxdb_bucket = os.getenv("INFLUXDB_BUCKET", "meinBucket")

# InfluxDB-Client initialisieren
influxdb_client = InfluxDBClient(url=f"http://{influxdb_host}:{influxdb_port}", token=influxdb_token, org=influxdb_org)
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

import json

import json

def process_message(msg):
    """
    Verarbeitet die eingehende MQTT-Nachricht und extrahiert Tags und Felder für InfluxDB.
    """
    topic_segments = msg.topic.split('/')
    tag_dict = {f"tag{i+1}": segment for i, segment in enumerate(topic_segments[:-1])}
    field_name = topic_segments[-1]
    try:
        field_value = float(msg.payload.decode())
    except ValueError:
        field_value = msg.payload.decode()

    #logger.info("tag_dict", tag_dict)
    #logger.info("field_namet", field_name)
    #logger.info("field_value", field_value)
    return tag_dict, field_name, field_value

def write_to_influxdb(tag_dict, field_name, field_value):
    """
    Schreibt Daten in die InfluxDB basierend auf den bereitgestellten Tags, Feldnamen und Feldwert.
    """
    point = Point("your_measurement")
    for tag_key, tag_value in tag_dict.items():
        point = point.tag(tag_key, tag_value)
    point = point.field(field_name, field_value)
    write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
    logger.info(f"Data written to InfluxDB: {field_value}, Tags: {tag_dict}, Field: {field_name}")
    #print(f"Data written to InfluxDB: {field_value}, Tags: {tag_dict}, Field: {field_name}")

def on_connect(client, userdata, flags, rc):
    logger.info("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    logger.info(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")
    tag_dict, field_name, field_value = process_message(msg)
    write_to_influxdb(tag_dict, field_name, field_value) 

def on_disconnect(client, userdata, rc):
    logger.warning("Disconnected from MQTT Broker")



# MQTT Client Setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message



try:
    mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)
    mqtt_client.loop_start()
    while True:  # Endlosschleife, um das Skript am Laufen zu halten
        pass
except KeyboardInterrupt:
    logger.info("MQTT-Bridge wird beendet.")
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
except Exception as e:
    logger.error("Ein Fehler ist aufgetreten: %s", str(e))
    mqtt_client.loop_stop()
