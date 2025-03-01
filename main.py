# main.py
from controllers.motor_controller import motors
from controllers.encoder_reader import EncoderReader
from controllers.movement import Movement, move_robot_with_vision
from utils.pid_manager import load_pid_params, update_pid_parameters
from controllers.pid_tuning import genetic_pid_tuning

def main():
    encoder_reader = EncoderReader()
    movement = Movement(motors)

    # Ajuste de PID
    for motor_name, motor in motors.items():
        genetic_pid_tuning(motor)
        kp, ki, kd = load_pid_params(motor_name)
        update_pid_parameters(motor, kp, ki, kd)

    # Inicia navegação com visão
    move_robot_with_vision()

if __name__ == "__main__":
    main()