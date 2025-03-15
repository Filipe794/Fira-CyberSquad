import pigpio
import time
from config import MOTOR_PINS
import threading

# TODO - se precisar, implementar um filtro melhor para a leitura do encoder

class EncoderReader:
    def __init__(self, motor_name, encoder_pin, max_history=10):
        self.motor_name = motor_name
        self.encoder_pin = encoder_pin
        self.encoder_count = 0
        self.last_time = time.time()
        self.lock = threading.Lock()
        self.encoder_history = []
        self.max_history = max_history
        
        # Inicializa a callback do encoder
        pi.callback(self.encoder_pin, pigpio.RISING_EDGE, self.encoder_callback)

        # Cria uma thread dedicada para monitorar a contagem do encoder
        self.read_thread = threading.Thread(target=self.read_encoder)
        self.read_thread.daemon = True
        self.read_thread.start()

    def encoder_callback(self, gpio, level, tick):
        # Incrementa a contagem do encoder a cada pulso
        with self.lock:
            self.encoder_count += 1

    def read_encoder(self):
        # Lê e processa os encoders em uma thread separada
        while True:
            now = time.time()
            dt = now - self.last_time
            self.last_time = now
            with self.lock:
                speed = self.encoder_count / dt
                self.encoder_count = 0
                # Suaviza a leitura com média móvel
                self.encoder_history.append(speed)
                if len(self.encoder_history) > self.max_history:
                    self.encoder_history.pop(0)

            time.sleep(0.05)  # Delay para evitar uso excessivo de CPU

    def get_speed(self):
        # Retorna a média das últimas leituras de velocidade
        if self.encoder_history:
            return sum(self.encoder_history) / len(self.encoder_history)
        return 0

# Inicializando os leitores de encoders para cada motor
encoder_readers = {
    motor: EncoderReader(motor, pins["encoder"])
    for motor, pins in MOTOR_PINS.items()
}
