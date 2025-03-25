import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pandas as pd
import cv2
import os
from sklearn.model_selection import train_test_split

# Diretório do dataset
DATASET_DIR = "dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
LABELS_FILE = os.path.join(DATASET_DIR, "labels.csv")

# Parâmetros
IMG_SIZE = (128, 128)  # Tamanho reduzido para melhorar desempenho
BATCH_SIZE = 32
EPOCHS = 10  # Ajuste conforme necessário

# carregar os dados
df = pd.read_csv(LABELS_FILE)
X, y = [], []

for _, row in df.iterrows():
    img_path = os.path.join(IMAGES_DIR, row["filename"])
    img = cv2.imread(img_path)
    img = cv2.resize(img, IMG_SIZE)  # Redimensiona para 128x128
    img = img / 255.0  # Normalização
    X.append(img)
    y.append(row["angle"])  # Ângulo real

X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.float32)

# Dividir em treino (80%) e validação (20%)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# criar o modelo de Transfer Learning
base_model = keras.applications.MobileNetV2(input_shape=(128, 128, 3), include_top=False, weights="imagenet")
base_model.trainable = False  # Congelar pesos para evitar overfitting

model = keras.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(64, activation="relu"),
    layers.Dense(1)
])

model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# treinar o modelo
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=EPOCHS, batch_size=BATCH_SIZE)

# converter para TensorFlow Lite para melhorar desempenho no Raspberry Pi
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# salvar modelo
with open("servo_model.tflite", "wb") as f:
    f.write(tflite_model)
