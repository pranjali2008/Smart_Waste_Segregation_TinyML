"""
Smart Waste Segregation - TinyML Model Training Script
-------------------------------------------------------
Trains a lightweight MobileNetV2-based image classifier for waste categories.
Converts the model to TensorFlow Lite (float32 and INT8 quantized) for edge deployment.

Usage:
    1. Organize dataset as:
           dataset/
           ├── paper/
           ├── plastic/
           ├── cardboard/
           ├── metal/
           ├── organic/
           └── battery/
    2. python train_waste_classifier.py

Author: Diploma Project Template
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, applications, optimizers, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from pathlib import Path

# ====================== CONFIGURATION ======================
DATASET_DIR = "dataset"                  # Path to your dataset folder
IMG_SIZE = (224, 224)                    # Input size for MobileNetV2
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.0001
NUM_CLASSES = None                       # Will be detected automatically
MODEL_SAVE_DIR = "../models"
RANDOM_SEED = 42

# Create output directory
Path(MODEL_SAVE_DIR).mkdir(parents=True, exist_ok=True)

# ====================== DATA PREPARATION ======================
def create_data_generators(dataset_dir, img_size, batch_size):
    """Create train and validation generators with augmentation."""
    
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=25,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2
    )

    val_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_generator = train_datagen.flow_from_directory(
        dataset_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        seed=RANDOM_SEED
    )

    val_generator = val_datagen.flow_from_directory(
        dataset_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        seed=RANDOM_SEED
    )

    return train_generator, val_generator


# ====================== MODEL BUILDING ======================
def build_model(num_classes, img_size, learning_rate):
    """Build MobileNetV2 transfer learning model."""
    
    base_model = applications.MobileNetV2(
        input_shape=(*img_size, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False          # Freeze base initially

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model, base_model


# ====================== TRAINING ======================
def train():
    print("=" * 60)
    print("Smart Waste Classifier - TinyML Training")
    print("=" * 60)

    if not os.path.exists(DATASET_DIR):
        print(f"\n[ERROR] Dataset folder '{DATASET_DIR}' not found!")
        print("Please create the folder and put class subfolders inside.")
        print("Example structure:")
        print("  dataset/paper/")
        print("  dataset/plastic/")
        print("  dataset/cardboard/")
        print("  dataset/metal/")
        print("  dataset/organic/")
        print("  dataset/battery/")
        return

    # Data generators
    train_gen, val_gen = create_data_generators(DATASET_DIR, IMG_SIZE, BATCH_SIZE)
    num_classes = len(train_gen.class_indices)
    class_names = list(train_gen.class_indices.keys())

    print(f"\nDetected {num_classes} classes: {class_names}")
    print(f"Training samples: {train_gen.samples}")
    print(f"Validation samples: {val_gen.samples}")

    # Build model
    model, base_model = build_model(num_classes, IMG_SIZE, LEARNING_RATE)
    model.summary()

    # Callbacks
    checkpoint_cb = callbacks.ModelCheckpoint(
        os.path.join(MODEL_SAVE_DIR, "best_waste_model.h5"),
        save_best_only=True,
        monitor='val_accuracy',
        mode='max',
        verbose=1
    )
    early_stop_cb = callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    reduce_lr_cb = callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-6,
        verbose=1
    )

    # Phase 1: Train head
    print("\n--- Phase 1: Training classification head ---")
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[checkpoint_cb, early_stop_cb, reduce_lr_cb]
    )

    # Phase 2: Fine-tune (optional)
    print("\n--- Phase 2: Fine-tuning last layers of base model ---")
    base_model.trainable = True
    # Freeze all layers except the last 30
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=optimizers.Adam(learning_rate=LEARNING_RATE / 10),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    history_fine = model.fit(
        train_gen,
        epochs=10,
        validation_data=val_gen,
        callbacks=[checkpoint_cb, early_stop_cb]
    )

    # Save final Keras model
    final_keras_path = os.path.join(MODEL_SAVE_DIR, "waste_classifier_final.h5")
    model.save(final_keras_path)
    print(f"\nKeras model saved to: {final_keras_path}")

    # ====================== CONVERT TO TFLITE ======================
    print("\n--- Converting to TensorFlow Lite ---")

    # Float32 TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    tflite_path = os.path.join(MODEL_SAVE_DIR, "waste_classifier_float32.tflite")
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    print(f"Float32 TFLite model saved: {tflite_path} ({os.path.getsize(tflite_path)/1024:.1f} KB)")

    # INT8 Quantized TFLite (recommended for microcontrollers)
    def representative_dataset():
        for _ in range(100):
            data = next(train_gen)[0]
            yield [data.astype(np.float32)]

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = representative_dataset
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.uint8
    converter.inference_output_type = tf.uint8

    tflite_quant_model = converter.convert()
    tflite_quant_path = os.path.join(MODEL_SAVE_DIR, "waste_classifier_int8.tflite")
    with open(tflite_quant_path, "wb") as f:
        f.write(tflite_quant_model)
    print(f"INT8 Quantized TFLite model saved: {tflite_quant_path} ({os.path.getsize(tflite_quant_path)/1024:.1f} KB)")

    # Save class labels
    labels_path = os.path.join(MODEL_SAVE_DIR, "labels.txt")
    with open(labels_path, "w") as f:
        for name in class_names:
            f.write(name + "\n")
    print(f"Class labels saved to: {labels_path}")

    # Plot training history
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'] + history_fine.history['accuracy'], label='Train Acc')
    plt.plot(history.history['val_accuracy'] + history_fine.history['val_accuracy'], label='Val Acc')
    plt.title('Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'] + history_fine.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'] + history_fine.history['val_loss'], label='Val Loss')
    plt.title('Loss')
    plt.legend()

    plot_path = os.path.join(MODEL_SAVE_DIR, "training_history.png")
    plt.savefig(plot_path)
    print(f"Training plot saved to: {plot_path}")

    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("Next steps:")
    print("  1. Test the model with: python infer_waste.py --image <path>")
    print("  2. For microcontroller deployment, prefer the INT8 .tflite model")
    print("  3. Or upload dataset to Edge Impulse for FOMO / further optimization")
    print("=" * 60)


if __name__ == "__main__":
    # Set seeds for reproducibility
    tf.random.set_seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    train()
