import cv2
import numpy as np

# TODO - implementar classe VisionSystem
# Precisa gerar o mapa para ser processado pelo path planning e pelo Pure Pursuit

class VisionSystem:
    def __init__(self, camera_index=0):
        self.camera = cv2.VideoCapture(camera_index)  # Inicializa a câmera
        if not self.camera.isOpened():
            print("Erro ao abrir a câmera")
            exit()

    def capture_frame(self):
        """
        Captura um único frame da câmera e converte para escala de cinza.
        """
        pass

    def detect_obstacles(self, frame):
        """
        Detecta obstáculos no frame fornecido e retorna a posição relativa.
        """
        pass

    def get_obstacle_data(self):
        pass

    def release(self):
        self.camera.release()
