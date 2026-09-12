# Suggested Components List & Approximate Cost (India, 2026)

| Component                        | Qty | Approx. Price (INR) | Remarks                          |
|----------------------------------|-----|---------------------|----------------------------------|
| ESP32-CAM Module                 | 1   | 400–600             | Best value for onboard TinyML    |
| Arduino Uno R3 (or clone)        | 1   | 400–700             | Main controller alternative      |
| SG90 Micro Servo                 | 3   | 150–250             | Flap control                     |
| DHT22 Temperature Humidity       | 1   | 200–300             | Decomposition monitoring         |
| Moisture Sensor Module           | 1   | 80–150              | Wet/Dry confirmation             |
| Inductive Proximity Sensor (NPN) | 1   | 150–300             | Metal detection                  |
| HC-SR04 Ultrasonic               | 2   | 100–150             | Bin fill level                   |
| 16x2 I2C LCD                     | 1   | 150–250             | Status display                   |
| Buzzer                           | 1   | 20–40               | Hazardous alert                  |
| 5V 2A Power Adapter              | 1   | 150–250             | System power                     |
| Jumper Wires, Breadboard, PCB    | -   | 100–200             | Prototyping                      |
| Mechanical (Acrylic/Wood/Bins)   | -   | 300–800             | Frame and collection bins        |
| **Total Approximate**            |     | **2000 – 4000**     | Depends on quality & sourcing    |

**Notes:**
- Prices are approximate and vary by seller (Robu, Amazon, local electronics markets).
- For pure TinyML focus, ESP32-CAM + 1–2 servos is sufficient for a working demo.
- Add camera stand / good lighting for reliable image classification.
