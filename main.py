from controllers.motor_controller import motors
from controllers.encoder_reader import EncoderReader
from controllers.movement import Movement
from utils.pid_manager import load_pid_params, update_pid_parameters
from controllers.pid_tuning import genetic_pid_tuning
from controllers.movement import move_robot_with_vision

# TODO - implementar lógica principal do robô
# TODO - Lidar com falha de sensores
# TODO - Interface de controle e visualização de dados em tempo real (se possivel, da pra ser web)
# TODO - Monitorar a carga da bateria

def main():
    # Inicializa os encoders para os motores
    encoder_reader = EncoderReader()
    
    # Inicializa o controle de movimento do robô
    movement = Movement(motors)

    # Ajuste de PID para todos os motores
    for motor_name, motor in motors.items():
        genetic_pid_tuning(motor)

        # Carrega os parâmetros otimizados
        kp, ki, kd = load_pid_params(motor_name)
        update_pid_parameters(motor, kp, ki, kd)
    

if __name__ == "__main__":
    main()