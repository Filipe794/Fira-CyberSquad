import cv2
from config import MOTOR_PINS, VISION_CONFIG, LASER_CONFIG
from controllers.motor_controller import MotorController
from vision.vision import VisionSystem

def setup_movement():
    motors = {
        name: MotorController(name, pins["pwm"], pins["dir"], pins["encoder"], None)
        for name, pins in MOTOR_PINS.items()
    }
    return motors

def set_robot_velocity_with_vision(motors, vision_system, vx=100, vy=0, omega=0):
    """
    Ajusta a velocidade do robô com base na visão computacional e sensor laser.
    """
    frame = vision_system.get_frame()
    obstacle_data = vision_system.get_obstacle_data(frame)

    if obstacle_data:
        distance = obstacle_data["distance"]
        center_point = obstacle_data["center_point"]
        all_centers = obstacle_data["all_centers"]

        # Lógica de navegação combinando visão e sensor laser
        if distance < LASER_CONFIG["safe_distance"]:  # Obstáculo detectado pelo laser
            vx = 0  # Para o movimento frontal
            omega = 50 if all_centers[0][0] < VISION_CONFIG["center_x"] else -50  # Gira baseado na visão
            print(f"Obstáculo a {distance}mm - ajustando direção")
        elif center_point and center_point[1] < VISION_CONFIG["obstacle_threshold"]:  # Obstáculo na visão
            min_y_center = min(all_centers, key=lambda p: p[1])
            if min_y_center[0] < VISION_CONFIG["center_x"]:
                omega = 50  # Gira à direita
            else:
                omega = -50  # Gira à esquerda
            vx = 0
        else:
            vx = 100  # Continua em frente
            omega = 0

        # Desenha linhas no frame para depuração (opcional)
        if center_point:
            center_x, center_y = center_point
            cv2.line(frame, (VISION_CONFIG["center_x"], VISION_CONFIG["bottom_y"]),
                     (center_x, center_y), (0, 255, 0), 3)
            for avg_x, avg_y in all_centers:
                cv2.line(frame, (VISION_CONFIG["center_x"], VISION_CONFIG["bottom_y"]),
                         (avg_x, avg_y), (255, 0, 0), 2)

    # Calcula velocidades dos motores
    speeds = {
        "front_left": vy + vx + omega,
        "front_right": vy - vx - omega,
        "rear_left": vy - vx + omega,
        "rear_right": vy + vx - omega,
    }

    # Limita a velocidade máxima
    max_speed = max(abs(s) for s in speeds.values())
    if max_speed > 255:
        speeds = {k: (v / max_speed) * 255 for k, v in speeds.items()}

    # Aplica as velocidades
    for motor_name, speed in speeds.items():
        motors[motor_name].set_speed(speed)

    return frame  # Retorna o frame processado para visualização

# Exemplo de uso
def move_robot_with_vision():
    motors = setup_movement()
    vision_system = VisionSystem(camera_index=0)
    try:
        while True:
            frame = set_robot_velocity_with_vision(motors, vision_system)
            cv2.imshow("Navigation", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        set_robot_velocity_with_vision(motors, vision_system, vx=0, vy=0, omega=0)
    finally:
        vision_system.release()