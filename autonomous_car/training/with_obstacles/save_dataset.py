import cv2
import csv
import os
import time
import random  # Simula leituras dos sensores (substitua pela leitura real)
import board
import busio
import adafruit_vl53l0x

# Diretórios para salvar o dataset
DATASET_DIR = "dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
LABELS_FILE = os.path.join(DATASET_DIR, "labels.csv")

# Criar pastas se não existirem
os.makedirs(IMAGES_DIR, exist_ok=True)

# Inicializar câmera
cap = cv2.VideoCapture(0)  # Use 0 para câmera padrão do Raspberry Pi

# Inicializar comunicação I2C com os sensores ToF
i2c = busio.I2C(board.SCL, board.SDA)

# Inicializar sensores ToF (frontal e lateral direito)
tof_front = adafruit_vl53l0x.VL53L0X(i2c)
tof_right = adafruit_vl53l0x.VL53L0X(i2c, address=0x30)  # Configure se precisar de outro endereço I2C

# Criar ou abrir o arquivo CSV para armazenar os dados
file_exists = os.path.isfile(LABELS_FILE)
with open(LABELS_FILE, mode="a", newline="") as file:
    writer = csv.writer(file)

    # Se o arquivo for novo, adicionar cabeçalhos
    if not file_exists:
        writer.writerow(["filename", "angle", "distance_front", "distance_right"])

    try:
        frame_count = 0
        print("Pressione 'q' para sair...")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar a imagem.")
                break

            # Simular leitura do ângulo do servo (substitua pelo código real)
            angle = random.uniform(-30, 30)  # Gera um ângulo aleatório (-30° a 30°)

            # Ler distâncias dos sensores ToF
            distance_front = tof_front.range  # Distância do sensor frontal (mm)
            distance_right = tof_right.range  # Distância do sensor lateral direito (mm)

            # Gerar nome da imagem
            image_name = f"frame_{frame_count:04d}.jpg"
            image_path = os.path.join(IMAGES_DIR, image_name)

            # Salvar imagem
            cv2.imwrite(image_path, frame)

            # Registrar no CSV
            writer.writerow([image_name, angle, distance_front, distance_right])
            print(f"Salvo: {image_name} | Ângulo: {angle:.2f}° | Distância Frontal: {distance_front} mm | Distância Direita: {distance_right} mm")

            frame_count += 1

            # Mostrar a imagem capturada
            cv2.imshow("Captura", frame)

            # Aguarda 100ms e permite sair com 'q'
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")

    finally:
        cap.release()
        cv2.destroyAllWindows()
