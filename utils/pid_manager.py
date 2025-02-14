import json
import os
from config import PID_CONFIG_FILE

def load_pid_params(motor_name):
    if os.path.exists(PID_CONFIG_FILE):
        with open(PID_CONFIG_FILE, "r") as f:
            data = json.load(f)
        motor_data = data.get(motor_name)
        if motor_data: # procura os parametros do motor
            return motor_data["Kp"], motor_data["Ki"], motor_data["Kd"]
        else: # retorna o padrão se não existirem parametros
            return 1.0, 0.1, 0.05
    else:
        return 1.0, 0.1, 0.05

def save_pid_params(motor_name, kp, ki, kd):
    if os.path.exists(PID_CONFIG_FILE):
        with open(PID_CONFIG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # parâmetros para o motor específico
    data[motor_name] = {"Kp": kp, "Ki": ki, "Kd": kd}

    with open(PID_CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_pid_parameters(motor, kp=None, ki=None, kd=None):
    if kp is not None:
        motor.pid.Kp = kp
    if ki is not None:
        motor.pid.Ki = ki
    if kd is not None:
        motor.pid.Kd = kd

    print("parâmetros atualizados")
