import json
import os
from config import PID_CONFIG_FILE

def load_pid_params(motor_name):
    """
    Carrega os parâmetros PID para o motor especificado.
    Caso o arquivo não exista ou haja erro na leitura, retorna os valores padrão.
    """
    if os.path.exists(PID_CONFIG_FILE):
        try:
            # Tenta abrir o arquivo e carregar os parâmetros
            with open(PID_CONFIG_FILE, "r") as f:
                data = json.load(f)
            motor_data = data.get(motor_name)
            if motor_data:
                return motor_data["Kp"], motor_data["Ki"], motor_data["Kd"]
            else:
                # Se o motor não tiver parâmetros salvos, retorna os padrões
                return 1.0, 0.1, 0.05
        except json.JSONDecodeError:
            # Caso o arquivo esteja corrompido, imprime erro e retorna os valores padrão
            print(f"Erro ao decodificar {PID_CONFIG_FILE}. Usando valores padrão.")
            return 1.0, 0.1, 0.05
    else:
        # Caso o arquivo não exista, retorna os valores padrão
        return 1.0, 0.1, 0.05

def save_pid_params(motor_name, kp, ki, kd):
    """
    Salva os parâmetros PID para o motor especificado no arquivo JSON.
    Caso o arquivo já exista, sobrescreve os valores.
    """
    backup_file = PID_CONFIG_FILE + ".bak"
    
    # Faz backup do arquivo atual antes de sobrescrever
    if os.path.exists(PID_CONFIG_FILE):
        os.rename(PID_CONFIG_FILE, backup_file)
    
    # Verifica se o arquivo de configuração existe, caso contrário cria um novo dicionário
    if os.path.exists(PID_CONFIG_FILE):
        with open(PID_CONFIG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Adiciona ou atualiza os parâmetros do motor
    data[motor_name] = {"Kp": kp, "Ki": ki, "Kd": kd}

    # Salva os dados no arquivo de configuração
    with open(PID_CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_pid_parameters(motor, kp=None, ki=None, kd=None):
    """
    Atualiza os parâmetros PID do motor com os valores fornecidos.
    Valida os parâmetros para garantir que são números válidos.
    """
    def is_valid_pid_param(param):
        """
        Verifica se o parâmetro é válido (número e maior ou igual a zero).
        """
        return isinstance(param, (int, float)) and param >= 0

    # Atualiza os parâmetros, caso sejam válidos
    if kp is not None and is_valid_pid_param(kp):
        motor.pid.Kp = kp
    if ki is not None and is_valid_pid_param(ki):
        motor.pid.Ki = ki
    if kd is not None and is_valid_pid_param(kd):
        motor.pid.Kd = kd

    # Confirma que os parâmetros foram atualizados
    print("parâmetros atualizados")
