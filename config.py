# Definição dos pinos dos motores
MOTOR_PINS = {
    "front_left": {"pwm": 17, "dir": 27, "encoder": 5},
    "front_right": {"pwm": 22, "dir": 23, "encoder": 6},
    "rear_left": {"pwm": 24, "dir": 25, "encoder": 13},
    "rear_right": {"pwm": 12, "dir": 16, "encoder": 19}
}

# Parâmetros do PID padrão (Kp, Ki, Kd)
DEFAULT_PID = {
    "Kp": 1.0,
    "Ki": 0.1,
    "Kd": 0.05
}

# Limites para o controle de PWM dos motores
PWM_LIMITS = {
    "min": 0,
    "max": 255
}

# Configurações gerais
PID_CONFIG_FILE = "pid_params.json"  # Arquivo onde os parâmetros do PID serão salvos/carregados

# Taxa de atualização do controlador PID (em segundos)
PID_UPDATE_INTERVAL = 0.05
