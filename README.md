# 🚀 IoT-Backbone

## 🌟 Überblick

Hey, IoT-Enthusiasten! Willkommen im Zentrum des digitalen Universums - dem IoT-Backbone. 🌍 Hier bringen wir Eclipse Mosquitto (den coolsten MQTT-Broker im Block), InfluxDB (die Zeitreihendatenbank Ihrer Träume) und eine selbstgebaute MQTT-InfluxDB-Brücke (der heimliche Star der Show) zusammen, alles verpackt in einem schicken Docker Compose-Setup. Perfekt für alles, was blinkt, piepst und Daten sendet. 🚦🤖

## 🚀 Features

Eclipse Mosquitto MQTT Broker: Sprechen Sie 'MQTT'? Er tut es definitiv! 📡
InfluxDB: Zeitreihendaten? Mehr wie Zeitreihenpartys! 🎉
MQTT-InfluxDB-Brücke: Der Brückenbauer, der MQTT und InfluxDB zusammenbringt - wie Peanutbutter und Jelly. 🥜🍇
🛠 Voraussetzungen

Docker und Docker Compose: Sei bereit, Container zu entern! 🐳
Eine Prise Neugier und eine Tasse Kaffee (oder Tee, wir diskriminieren nicht) ☕
## 🚀 Installation und Setup

Klonen, als gäbe es kein Morgen:
```bash
git clone https://github.com/8uddy/IoT-Backbone
cd IoT-Backbone
```
Geheime .env-Datei (shh, nicht weitersagen!):
Kopiere .env.example zu .env und füge deine Geheimnisse hinzu. 🔒
```dotenv
# .env Konfigurationsdatei

# Mosquitto MQTT Broker Einstellungen
MOSQUITTO_PORT=1883
MOSQUITTO_WS_PORT=9001

# Node-RED Einstellungen (falls verwendet)
NODERED_PORT=1880

# MQTT Topic, das überwacht werden soll
MQTT_TOPIC=Ihr/MQTT/Topic

# InfluxDB Einstellungen
INFLUXDB_PORT=8086
INFLUXDB_USERNAME=IhrUsername
INFLUXDB_PASSWORD=IhrPasswort
INFLUXDB_ORG=IhreOrganisation
INFLUXDB_BUCKET=IhrBucket
INFLUXDB_TOKEN=IhrInfluxDBToken
```

Abheben mit Docker Compose:

```bash
docker-compose up -d
```

## 📐 Konfiguration

Hier erklären wir, wie man Dinge umstellt, dreht und wendet, bis sie perfekt sind. 🎛️

##  💡 Nutzung

So, wie spricht man mit einer IoT-Backbone? Spoiler: Es beinhaltet viel Tippen und ein bisschen Magie. ✨

##  🤝 Beitrag

Willst du ein Teil der Legende werden? Schau in CONTRIBUTING.md rein und zeig uns, was du drauf hast! 🦸‍♀️🦸‍♂️

##  📜 Lizenz

Frei wie der Wind unter der MIT Lizenz. 🌬️

##  📬 Support und Kontakt

Fragen, Gedanken, existenzielle Krisen? Eröffne ein Issue oder kontaktiere uns – wir beißen nicht, versprochen! 🤗