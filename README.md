# ESP32 MQTT NeoPixel Touch Controller

This project connects an ESP32 microcontroller to WiFi and an MQTT broker to control an RGB LED strip (NeoPixel) using touch inputs. The touch sensor on the ESP32 detects input and sends the state via MQTT. This can be used to synchronize touch-based LED control across multiple devices.

## Features

- **WiFi and MQTT Integration**: Connects to a WiFi network and an MQTT broker to publish touch state data.
- **NeoPixel Control**: Controls an RGB LED strip with customizable colors for each LED.
- **Touch Sensor**: Detects touch input on GPIO4 (T0) and publishes the state to MQTT.
- **Device ID**: Uses a unique device ID for each ESP32 to differentiate between devices on the MQTT network.

## Hardware Requirements

- ESP32 Development Board
- NeoPixel LED Strip (8 LEDs)
- Capacitive Touch Sensor on GPIO4 (T0)

## Software Requirements

- Arduino IDE (or PlatformIO)
- Libraries:
  - [WiFi](https://www.arduino.cc/en/Reference/WiFi)
  - [PubSubClient](https://github.com/knolleary/pubsubclient)
  - [Adafruit NeoPixel](https://github.com/adafruit/Adafruit_NeoPixel)

## Wiring Diagram

| ESP32 Pin | NeoPixel Pin | Function           |
|-----------|--------------|--------------------|
| 15        | DIN          | NeoPixel Data Pin |
| GND       | GND          | Ground            |
| 5V        | VCC          | Power             |

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/esp32-mqtt-neopixel-touch
    ```
2. **Install required libraries** in Arduino IDE (WiFi, PubSubClient, and Adafruit NeoPixel).

3. **Configure the Code:**
   - Set your WiFi credentials:
     ```cpp
     const char* ssid = "your-SSID";
     const char* password = "your-password";
     ```
   - Configure the MQTT broker details:
     ```cpp
     const char* mqtt_broker = "broker.emqx.io";
     const int mqtt_port = 1883;
     const char* topic_touch_state = "your-topic/touch_state";
     ```

## Code Explanation

- **setup_wifi()**: Connects the ESP32 to the WiFi network.
- **callback()**: Handles incoming MQTT messages for touch state updates.
- **reconnect()**: Reconnects to the MQTT broker if the connection is lost.
- **setup()**: Initializes the NeoPixel, WiFi, and MQTT client.
- **loop()**: Reads the touch sensor value, publishes the state via MQTT, and controls the NeoPixel LEDs based on the received state.

## Usage

1. **Upload the code** to the ESP32.
2. On touching the sensor, the device publishes the touch state to the MQTT broker.
3. Another ESP32 subscribed to the same topic will synchronize its LED strip with the published state.

## Troubleshooting

- Ensure correct wiring and power supply for the NeoPixel.
- Check that the MQTT broker is online and reachable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
