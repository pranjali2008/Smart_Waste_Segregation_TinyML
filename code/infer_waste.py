"""
Smart Waste Segregation - TinyML Inference Script
-------------------------------------------------
Loads a trained TFLite model and classifies waste images.
Can run on a single image or live webcam feed (for demonstration).

Usage:
    python infer_waste.py --image path/to/image.jpg
    python infer_waste.py --webcam
    python infer_waste.py --image path/to/image.jpg --model ../models/waste_classifier_int8.tflite
"""

import argparse
import os
import numpy as np
import tensorflow as tf
from PIL import Image
import cv2
from pathlib import Path

# ====================== CONFIGURATION ======================
DEFAULT_MODEL = "../models/waste_classifier_float32.tflite"
DEFAULT_LABELS = "../models/labels.txt"
IMG_SIZE = (224, 224)


def load_labels(labels_path):
    """Load class labels from text file."""
    if not os.path.exists(labels_path):
        # Fallback default labels
        return ["paper", "plastic", "cardboard", "metal", "organic", "battery"]
    with open(labels_path, "r") as f:
        labels = [line.strip() for line in f.readlines()]
    return labels


def load_tflite_model(model_path):
    """Load TFLite model and allocate tensors."""
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter


def preprocess_image(image_path, img_size, input_details):
    """Load and preprocess image for the model."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(img_size)
    img_array = np.array(img, dtype=np.float32)

    # Check if model expects quantized input (uint8)
    if input_details[0]['dtype'] == np.uint8:
        img_array = img_array.astype(np.uint8)
    else:
        img_array = img_array / 255.0
        img_array = img_array.astype(np.float32)

    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def preprocess_frame(frame, img_size, input_details):
    """Preprocess OpenCV frame."""
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, img_size)
    img_array = np.array(img, dtype=np.float32)

    if input_details[0]['dtype'] == np.uint8:
        img_array = img_array.astype(np.uint8)
    else:
        img_array = img_array / 255.0
        img_array = img_array.astype(np.float32)

    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict(interpreter, input_data):
    """Run inference and return probabilities."""
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])[0]

    # Dequantize if necessary
    if output_details[0]['dtype'] == np.uint8:
        scale, zero_point = output_details[0]['quantization']
        output = scale * (output.astype(np.float32) - zero_point)

    return output


def classify_image(model_path, labels_path, image_path):
    """Classify a single image and print results."""
    print(f"\nLoading model: {model_path}")
    interpreter = load_tflite_model(model_path)
    input_details = interpreter.get_input_details()
    labels = load_labels(labels_path)

    print(f"Processing image: {image_path}")
    input_data = preprocess_image(image_path, IMG_SIZE, input_details)
    probabilities = predict(interpreter, input_data)

    # Get top prediction
    top_idx = np.argmax(probabilities)
    confidence = probabilities[top_idx] * 100

    print("\n" + "=" * 50)
    print("CLASSIFICATION RESULT")
    print("=" * 50)
    print(f"Predicted Class : {labels[top_idx].upper()}")
    print(f"Confidence      : {confidence:.2f}%")
    print("\nAll class probabilities:")
    for i, (label, prob) in enumerate(zip(labels, probabilities)):
        print(f"  {label:12s} : {prob*100:6.2f}%")
    print("=" * 50)

    # Suggested action for the segregation system
    action = get_segregation_action(labels[top_idx])
    print(f"\nSuggested Action: {action}")
    return labels[top_idx], confidence


def get_segregation_action(predicted_class):
    """Map class to physical action (servo angle / bin)."""
    mapping = {
        "paper":      "Servo → Dry/Recyclable Bin (Angle 0°)",
        "cardboard":  "Servo → Dry/Recyclable Bin (Angle 0°)",
        "plastic":    "Servo → Dry/Recyclable Bin (Angle 90°)",
        "metal":      "Servo → Metal Bin (Angle 180°)",
        "organic":    "Servo → Wet/Organic → Decomposition Chamber",
        "battery":    "BUZZER ALERT + Special Hazardous Handling",
    }
    return mapping.get(predicted_class.lower(), "Unknown - Manual check required")


def run_webcam(model_path, labels_path):
    """Live webcam classification demo."""
    print("\nStarting webcam demo... Press 'q' to quit.")
    interpreter = load_tflite_model(model_path)
    input_details = interpreter.get_input_details()
    labels = load_labels(labels_path)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        input_data = preprocess_frame(frame, IMG_SIZE, input_details)
        probabilities = predict(interpreter, input_data)
        top_idx = np.argmax(probabilities)
        confidence = probabilities[top_idx] * 100
        label = labels[top_idx]

        # Draw result on frame
        text = f"{label.upper()}: {confidence:.1f}%"
        color = (0, 255, 0) if confidence > 70 else (0, 165, 255)
        cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, get_segregation_action(label)[:40], (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow("Smart Waste Classifier - TinyML", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="TinyML Waste Classification Inference")
    parser.add_argument("--image", type=str, help="Path to input image")
    parser.add_argument("--webcam", action="store_true", help="Run live webcam demo")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Path to .tflite model")
    parser.add_argument("--labels", type=str, default=DEFAULT_LABELS, help="Path to labels.txt")

    args = parser.parse_args()

    if not os.path.exists(args.model):
        print(f"[ERROR] Model file not found: {args.model}")
        print("Please train a model first using train_waste_classifier.py")
        print("Or place a pre-trained .tflite model in the models/ folder.")
        return

    if args.webcam:
        run_webcam(args.model, args.labels)
    elif args.image:
        if not os.path.exists(args.image):
            print(f"[ERROR] Image not found: {args.image}")
            return
        classify_image(args.model, args.labels, args.image)
    else:
        print("Please provide either --image <path> or --webcam")
        parser.print_help()


if __name__ == "__main__":
    main()
