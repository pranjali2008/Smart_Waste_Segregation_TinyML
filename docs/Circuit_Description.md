# Circuit & Interfacing Description

## Main Controller Options
1. **Recommended for students**: ESP32-CAM (camera + Wi-Fi + enough power for TinyML FOMO models)
2. Alternative: Arduino Uno / Nano + external camera module + host computer for inference
3. Advanced: Arduino UNO Q or Nano 33 BLE Sense with camera

## Sensor Connections (Arduino Uno example)

| Sensor / Actuator       | Arduino Pin     | Notes                              |
|-------------------------|-----------------|------------------------------------|
| Moisture Sensor (Analog)| A0              | Calibrate threshold empirically    |
| Metal / Inductive Sensor| D7 (Digital)    | HIGH when metal detected           |
| DHT22 (Temp + Humidity) | D6              | Use DHT library                    |
| Servo - Dry Bin         | D9              | PWM capable                        |
| Servo - Metal Bin       | D10             | PWM capable                        |
| Servo - Organic Bin     | D11             | PWM capable                        |
| Buzzer                  | D8              | Active or passive                  |
| Ultrasonic Trig         | D4              | Optional fill level                |
| Ultrasonic Echo         | D5              | Optional fill level                |
| I2C LCD (SDA/SCL)       | A4 / A5         | Optional status display            |

## Power Considerations
- Servos can draw significant current → use external 5V supply (2A or more) with common ground.
- ESP32-CAM prefers 5V regulated supply.
- Never power high-current devices directly from Arduino 5V pin.

## Decomposition Chamber
- Place DHT22 sensor inside or near the organic waste chamber.
- Optional: small 5V fan for aeration controlled by a MOSFET / relay on a free digital pin.
- Optional: heating element with temperature control (more advanced).

## Communication
- Serial (USB) between host Python script and Arduino for demonstration.
- For standalone: run TinyML inference directly on ESP32-CAM / Nano 33 BLE and control servos locally.
