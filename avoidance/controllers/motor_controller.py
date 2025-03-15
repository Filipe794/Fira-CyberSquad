import time
import pigpio
import threading
from simple_pid import PID
from config import MOTOR_PINS, PWM_LIMITS, PID_UPDATE_INTERVAL
from utils.pid_manager import load_pid_params
from laser_sensor import DistanceSensor

# Inicializa o Raspberry Pi GPIO com pigpio
pi = pigpio.pi()

# Função para configurar os pinos dos motores
def setup_motors():
    for motor, pins in MOTOR_PINS.items():
        pi.set_mode(pins["pwm"], pigpio.OUTPUT)
        pi.set_mode(pins["dir"], pigpio.OUTPUT)
        pi.set_mode(pins["encoder"], pigpio.INPUT)
        pi.set_pull_up_down(pins["encoder"], pigpio.PUD_UP)

# Classe para controle de motores com PID
class MotorController:
    def __init__(self, name, pwm_pin, dir_pin, encoder_pin, distance_sensor):
        self.name = name
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.encoder_pin = encoder_pin
        self.speed = 0
        self.target_speed = 0
        self.encoder_count = 0
        self.last_time = time.time()

        # Carregar parâmetros PID do arquivo JSON (se existir)
        pid_params = load_pid_params(name)
        kp, ki, kd = pid_params if pid_params else (1.0, 0.1, 0.05)

        # Inicializa o PID com os parâmetros carregados ou padrão
        self.pid = PID(kp, ki, kd, setpoint=0)
        self.pid.output_limits = (PWM_LIMITS["min"], PWM_LIMITS["max"])

        # Configura a callback para o encoder
        pi.callback(self.encoder_pin, pigpio.RISING_EDGE, self.encoder_callback)

        # Thread para controle do motor
        self.control_thread = threading.Thread(target=self.update_motor)
        self.control_thread.daemon = True
        self.control_thread.start()

    def encoder_callback(self, gpio, level, tick):
        self.encoder_count += 1

    def calculate_speed(self):
        # Calcula a velocidade com base nos encoders
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        speed = self.encoder_count / dt
        self.encoder_count = 0
        return speed

    def update_motor(self):
        # Atualiza a velocidade do motor com PID
        while True:
            speed = self.calculate_speed()
            control = self.pid(speed)
            self.set_motor_pwm(control)

            # Verifica a distância para ajustar o comportamento do robô
            distance = self.distance_sensor.get_distance()
            if distance < 200:  # Se a distância for menor que 200mm, desacelera ou para
                print(f"Obstáculo detectado a {distance}mm! Desacelerando...")
                self.set_speed(0)  # Ou outro comportamento de evasão

            time.sleep(PID_UPDATE_INTERVAL)

    def set_motor_pwm(self, pwm_value):
        # Ajusta o PWM do motor com base no valor calculado
        direction = 1 if pwm_value >= 0 else 0
        pwm_value = min(abs(int(pwm_value)), PWM_LIMITS["max"])
        pi.write(self.dir_pin, direction)
        pi.set_PWM_dutycycle(self.pwm_pin, pwm_value)

    def set_speed(self, speed):
        # Define a velocidade alvo para o PID
        self.pid.setpoint = speed

# Inicializa o sensor de distância
distance_sensor = DistanceSensor()

# Inicializa os motores
setup_motors()

# Criação dos controladores de motor
motors = {
    name: MotorController(name, pins["pwm"], pins["dir"], pins["encoder"], distance_sensor)
    for name, pins in MOTOR_PINS.items()
}