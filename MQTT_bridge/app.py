import paho.mqtt.client as mqtt
import logging
import os
import json
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import logging
from logging.handlers import RotatingFileHandler
import os

# Logging-Konfiguration
log_file_path = os.path.join(os.getcwd(), 'mqtt_bridge.log')  # Pfad zur Log-Datei
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Formatierung der Log-Nachrichten

# FileHandler für die Ausgabe in eine Datei
file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)  # 10 MB pro Datei, 5 Backup-Dateien
file_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Setzt das Level des Loggers
logger.addHandler(file_handler)  # Fügt den FileHandler zum Logger hinzu


# Umgebungsvariablen
mqtt_broker_host = os.getenv("MQTT_BROKER_HOST", "172.21.0.2")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT", "1883"))
mqtt_topic = os.getenv("MQTT_TOPIC", "AWS11/#")

# InfluxDB-Verbindungseinstellungen
influxdb_host = os.getenv("INFLUXDB_HOST", "172.21.0.4")
influxdb_port = int(os.getenv("INFLUXDB_PORT", "8086"))
influxdb_token = os.getenv("INFLUXDB_TOKEN")
influxdb_org = os.getenv("INFLUXDB_ORG","meineOrganisation")  # Stellen Sie sicher, dass diese Zeile korrekt ist
influxdb_bucket = os.getenv("INFLUXDB_BUCKET", "iot-raw")

# InfluxDB-Client initialisieren
influxdb_client = InfluxDBClient(url=f"http://{influxdb_host}:{influxdb_port}", token=influxdb_token, org=influxdb_org)
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)


def process_message(msg):
    """
    Verarbeitet die eingehende MQTT-Nachricht und extrahiert Tags, Felder und Timestamp für InfluxDB.
    """
    topic_segments = msg.topic.split('/')
    tag_dict = {f"tag{i+1}": segment for i, segment in enumerate(topic_segments)}

    try:
        payload = json.loads(msg.payload.decode())

        field_dict = {}
        for k, v in payload.items():
            if k != "_timestamp":
                if k == "target":
                    try:
                        field_dict[k] = float(v) if v is not None else None
                    except ValueError:
                        field_dict[k] = str(v)
                elif v is None:
                    continue
                elif isinstance(v, (dict, list)):
                    field_dict[k] = json.dumps(v)
                else:
                    try:
                        field_dict[k] = int(v)
                    except (ValueError, TypeError):
                        try:
                            field_dict[k] = float(v) if v is not None else None
                        except ValueError:
                            field_dict[k] = v

        timestamp = payload.get("_timestamp", int(time.time()))
    except json.JSONDecodeError:
        field_dict = {"value": msg.payload.decode()}
        timestamp = int(time.time())

    return tag_dict, field_dict, timestamp





def format_line_protocol(tag_dict, field_dict, timestamp):
    """
    Formatieren der Daten im Line Protocol.
    """
    # Konvertieren des Zeitstempels in Nanosekunden
    timestamp_ns = timestamp * 1000000000

    # Erstellen der Tag-String
    tags = ','.join([f"{key}={value}" for key, value in tag_dict.items()])

    # Erstellen der Felder-String
    fields = ','.join([f'{key}={value}' if isinstance(value, (int, float))
                       else f'{key}="{value}"' for key, value in field_dict.items()])

    # Zusammenfügen des Line Protocols
    line = f"mqtt,{tags} {fields} {timestamp_ns}"
    return line


def write_to_influxdb(line):
    """
    Schreibt Daten in die InfluxDB basierend auf dem Line Protocol.
    """
    try:
        write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=line)
        logger.info(f"Data written to InfluxDB using Line Protocol: {line}")
        return True
    except influxdb_client.exceptions.InfluxDBError as e:
        logger.error(f"InfluxDB API error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error writing to InfluxDB: {e}")
        return False

# Änderung in der on_message-Funktion
def on_message(client, userdata, msg):
    logger.info(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")
    tag_dict, field_dict, timestamp = process_message(msg)
    line = format_line_protocol(tag_dict, field_dict, timestamp)
    write_to_influxdb(line)


# Restliche Funktionen (on_connect, on_message) bleiben unverändert
def on_connect(client, userdata, flags, rc):
    logger.info("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_disconnect(client, userdata, rc):
    logger.warning("Disconnected from MQTT Broker")



# MQTT Client Setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message
logger.info("MQTT Client Setup")


try:
    mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, 60)
    mqtt_client.loop_start()
    logger.info("MQTT Client loop start")
    while True:  # Endlosschleife, um das Skript am Laufen zu halten
        pass
except KeyboardInterrupt:
    logger.info("MQTT-Bridge wird beendet.")
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
except Exception as e:
    logger.error("Ein Fehler ist aufgetreten: %s", str(e))
    mqtt_client.loop_stop()
