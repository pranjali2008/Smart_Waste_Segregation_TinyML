# Smart Waste Segregation and Decomposition System with TinyML

**Diploma / Final Year Project**  
**Title:** Smart Automated Waste Segregation Bin with TinyML Classification and Inbuilt Organic Waste Decomposer

---

## 1. Project Overview

This project develops a smart waste management system that automatically classifies waste using **TinyML (Edge AI image classification)** and traditional sensors, then segregates it into appropriate bins. Organic (wet) waste is directed to a decomposition chamber equipped with sensors for monitoring the composting process.

The system reduces manual sorting, improves recycling rates, and produces usable compost while teaching embedded systems, computer vision, IoT, and sustainability concepts.

### Key Features
- TinyML-based image classification (Paper, Plastic, Cardboard, Metal, Organic, Battery)
- Hybrid sensing (Moisture + Metal + Vision)
- Automatic segregation using servo motors
- Decomposition chamber with temperature & humidity monitoring
- Optional IoT dashboard for remote monitoring
- Fully documented for diploma submission

---

## 2. Objectives
1. Automatically classify waste using a lightweight TinyML model running on edge hardware.
2. Segregate waste into Metal, Wet/Organic, Dry/Recyclable, and Hazardous categories.
3. Direct organic waste into a controlled decomposition chamber.
4. Monitor compost parameters (temperature, humidity) and indicate readiness.
5. Provide a complete, low-cost, reproducible prototype suitable for diploma evaluation.

---

## 3. System Architecture

**Waste Input → Presence Detection → Image Capture → TinyML Inference → Classification Decision → Servo Actuation → Bin Routing**

- Organic waste → Decomposition Chamber (with DHT sensor monitoring)
- Metal / Dry / Hazardous → Respective bins
- Optional: Ultrasonic sensors for bin fill-level + IoT alerts

---

## 4. Hardware Components

| Component                  | Quantity | Purpose                              |
|---------------------------|----------|--------------------------------------|
| ESP32-CAM or Arduino UNO Q / Nano 33 BLE Sense + Camera | 1 | Image capture + TinyML inference    |
| Arduino Uno / ESP32       | 1        | Main controller & servo control      |
| SG90 / MG995 Servo Motors | 2–3      | Segregation flaps / rotating platform|
| Moisture Sensor           | 1        | Wet vs Dry confirmation              |
| Inductive Proximity Sensor| 1        | Metal detection                      |
| DHT11 / DHT22             | 1        | Temperature & Humidity in decomposer |
| Ultrasonic HC-SR04        | 2–3      | Bin fill level                       |
| 16x2 LCD / OLED           | 1        | Local status display                 |
| Buzzer                    | 1        | Hazardous item alert                 |
| Power Supply (5V/12V)     | 1        | System power                         |
| Mechanical Frame + Bins   | -        | Structure and collection             |

**Recommended for TinyML:** ESP32-CAM (cheapest) or Arduino UNO Q + USB camera for easier Python integration.

---

## 5. Software Stack

- **Model Training:** TensorFlow / Keras + Transfer Learning (MobileNetV2)
- **Deployment:** TensorFlow Lite / Edge Impulse (recommended for students)
- **Controller:** Arduino IDE (C++) + optional Python host scripts
- **IoT (Optional):** Blynk / ThingSpeak / MQTT
- **Languages:** Python (training & simulation), C++ (embedded)

---

## 6. Project Structure

```
Smart_Waste_Segregation_TinyML/
├── README.md                 # This file
├── docs/
│   ├── Project_Report_Outline.md
│   ├── Abstract.txt
│   └── Circuit_Description.md
├── code/
│   ├── train_waste_classifier.py      # Train TinyML model
│   ├── infer_waste.py                 # Run inference (simulation / host)
│   ├── requirements.txt
│   └── arduino/
│       └── waste_segregator.ino       # Main Arduino sketch
├── models/                   # Place trained .tflite models here
├── dataset_sample/           # Sample data organization
└── hardware/
    └── components_list.md
```

---

## 7. How to Use the Python Code

### Installation
```bash
cd code
pip install -r requirements.txt
```

### Training a Model
1. Organize your dataset as:
   ```
   dataset/
   ├── paper/
   ├── plastic/
   ├── cardboard/
   ├── metal/
   ├── organic/
   └── battery/
   ```
2. Run:
   ```bash
   python train_waste_classifier.py
   ```
3. The script will train a MobileNetV2-based model, convert it to TensorFlow Lite, and save it in the `models/` folder.

### Running Inference (Demo / Simulation)
```bash
python infer_waste.py --image path/to/test_image.jpg
```
or for webcam:
```bash
python infer_waste.py --webcam
```

---

## 8. Expected Results
- Classification accuracy: 85–95% on well-lit, clear images (depends on dataset quality)
- Model size: < 3–5 MB (float) → < 1 MB after INT8 quantization
- Inference time: Suitable for real-time on ESP32 / Arduino-class devices when optimized via Edge Impulse

---

## 9. Future Scope
- Deploy fully on ESP32-CAM using Edge Impulse FOMO
- Add continuous learning / online fine-tuning
- Integrate biogas generation with the decomposer
- Mobile app for user feedback and rewards
- Multi-bin robotic sorting arm

---

## 10. References & Acknowledgements
- Edge Impulse documentation and public waste sorting projects
- TensorFlow Lite for Microcontrollers
- TrashNet and similar public waste datasets
- Previous Arduino-based segregation and composting projects

---

**Prepared for Diploma Engineering Students**  
Feel free to modify classes, add sensors, or expand the mechanical design according to your college guidelines.
