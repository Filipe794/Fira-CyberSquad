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

# 1️⃣ Carregar os dados
df = pd.read_csv(LABELS_FILE)
X_img, X_dist, y = [], [], []

for _, row in df.iterrows():
    # Carregar e processar as imagens
    img_path = os.path.join(IMAGES_DIR, row["filename"])
    img = cv2.imread(img_path)
    img = cv2.resize(img, IMG_SIZE)  # Redimensiona para 128x128
    img = img / 255.0  # Normalização
    X_img.append(img)

    # Carregar e processar as distâncias dos sensores
    distance_front = row["distance_front"]  # Distância do sensor frontal
    distance_right = row["distance_right"]  # Distância do sensor lateral direito
    X_dist.append([distance_front, distance_right])

    # Carregar o ângulo
    y.append(row["angle"])

X_img = np.array(X_img, dtype=np.float32)
X_dist = np.array(X_dist, dtype=np.float32)
y = np.array(y, dtype=np.float32)

# Dividir em treino (80%) e validação (20%)
X_img_train, X_img_val, X_dist_train, X_dist_val, y_train, y_val = train_test_split(X_img, X_dist, y, test_size=0.2, random_state=42)

# 2️⃣ Criar o modelo de Transfer Learning com entrada adicional para as distâncias
base_model = keras.applications.MobileNetV2(input_shape=(128, 128, 3), include_top=False, weights="imagenet")
base_model.trainable = False  # Congelar pesos para evitar overfitting

# Entrada para as imagens
image_input = layers.Input(shape=(128, 128, 3))

# Passar as imagens pela MobileNetV2
x = base_model(image_input)
x = layers.GlobalAveragePooling2D()(x)

# Entrada para as distâncias
distance_input = layers.Input(shape=(2,))  # Dois sensores de distância (frontal e direito)
y = layers.Dense(32, activation="relu")(distance_input)

# Concatenar as saídas de imagem e distância
concatenated = layers.concatenate([x, y])

# Camada densa para regressão
z = layers.Dense(64, activation="relu")(concatenated)
output = layers.Dense(1)(z)  # Saída contínua (ângulo do servo)

# Criar o modelo
model = keras.Model(inputs=[image_input, distance_input], outputs=output)

model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# 3️⃣ Treinar o modelo
model.fit([X_img_train, X_dist_train], y_train, validation_data=([X_img_val, X_dist_val], y_val), epochs=EPOCHS, batch_size=BATCH_SIZE)

# 4️⃣ Converter para TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Salvar o modelo
with open("servo_model_with_sensors.tflite", "wb") as f:
    f.write(tflite_model)

print("Modelo treinado e salvo como servo_model_with_sensors.tflite ✅")
