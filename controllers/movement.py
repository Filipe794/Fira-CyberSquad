from config import MOTOR_PINS
from controllers.motor_controller import MotorController
from controllers.vision import VisionSystem

# TODO - implementar lógica de movimentação baseada na detecção de obstáculos (VIsão e Sensores VL53L0X)

def setup_movement():
    motors = {
        name: MotorController(name, pins["pwm"], pins["dir"], pins["encoder"])
        for name, pins in MOTOR_PINS.items()
    }
    return motors

def set_robot_velocity_with_vision(motors, vision_system, vx, vy, omega):
    """
    Ajusta a velocidade do robô com base nas informações da visão computacional.

    :param motors: Dicionário de motores
    :param vision_system: Instância do sistema de visão computacional
    :param vx: Velocidade em x (frente/trás)
    :param vy: Velocidade em y (esquerda/direita)
    :param omega: Velocidade angular (giro)
    """
    
    # Obtém os dados de obstáculos da visão computacional
    obstacle_positions = vision_system.get_obstacle_data()
    
    if obstacle_positions:
        
        # Ajusta o movimento dependendo da posição dos obstáculos
        for pos in obstacle_positions:
            pass

    # Calcula as velocidades dos motores com base nos ajustes feitos
    speeds = {
        "front_left": vy + vx + omega,
        "front_right": vy - vx - omega,
        "rear_left": vy - vx + omega,
        "rear_right": vy + vx - omega,
    }

    # Limita a velocidade máxima dos motores
    max_speed = max(abs(s) for s in speeds.values())
    if max_speed > 255:
        for key in speeds:
            speeds[key] = (speeds[key] / max_speed) * 255

    # Define as velocidades desejadas para cada motor
    for motor_name, speed in speeds.items():
        motors[motor_name].set_speed(speed)

''' - Exemplo de uso

def move_robot_with_vision():
    motors = setup_movement()
    vision_system = VisionSystem(camera_index=0)  # inicia o sistema de visão

    try:
        while True:
            set_robot_velocity_with_vision(motors, vision_system, vx=100, vy=0, omega=0)
    except KeyboardInterrupt:
        set_robot_velocity_with_vision(motors, vision_system, vx=0, vy=0, omega=0)
        vision_system.release()

'''
