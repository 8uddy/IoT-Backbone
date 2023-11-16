## README for Docker and Python MQTT_Bridge

## Dockerfile
- Base Image: Use python:3.10.
- Working Directory: Set to /app.
- Copy Dependencies: Add requirements.txt.
- Install Dependencies: Use pip install.
- Copy Application Files: Add your application files.
- Run Application: Start with python app.py.
## Python Script
- Logging: Configure logging with file rotation.
- Environment Variables: Read settings for MQTT and InfluxDB.
- InfluxDB Client: Initialize client.
- Message Processing: Process MQTT messages and format for InfluxDB.
- MQTT Client: Setup client and callback functions.
- Main Loop: Run an infinite loop, handle interruptions and errors.
## Usage
- Build Image: Execute docker build -t your-image-name ..
- Start Container: Use docker run -d --name your-container-name your-image-name.