import cv2
import csv
import os
import time
import random

DATASET_DIR = "dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
LABELS_FILE = os.path.join(DATASET_DIR, "labels.csv")

os.makedirs(IMAGES_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)

# criar ou abrir o arquivo csv
file_exists = os.path.isfile(LABELS_FILE)
with open(LABELS_FILE, mode="a", newline="") as file:
    writer = csv.writer(file)
    
    if not file_exists:
        writer.writerow(["filename", "angle"])

    try:
        frame_count = 0
        print("Pressione 'q' para sair...")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar a imagem.")
                break

            # substituir pela leitura real do motor servo
            angle = random.uniform(-30, 30)

            image_name = f"frame_{frame_count:04d}.jpg"
            image_path = os.path.join(IMAGES_DIR, image_name)

            cv2.imwrite(image_path, frame)

            # salvar no dataset
            writer.writerow([image_name, angle])
            print(f"Salvo: {image_name} | Ângulo: {angle:.2f}°")

            frame_count += 1

            # cv2.imshow("Captura", frame)

            # Aguarda 100ms e permite sair com 'q'
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")

    finally:
        cap.release()
        cv2.destroyAllWindows()