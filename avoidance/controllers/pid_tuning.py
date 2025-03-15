import random
import time
from utils.pid_manager import load_pid_params, save_pid_params

"""
Avalia o desempenho do PID com base nos parâmetros fornecidos.
:param kp: Parâmetro Kp do PID
:param ki: Parâmetro Ki do PID
:param kd: Parâmetro Kd do PID
:param motor: O objeto do motor a ser avaliado
:return: Diferença entre setpoint e velocidade real
"""

# Função de avaliação (fitness) - calcula o erro médio do PID
def evaluate_pid(kp, ki, kd, motor, evaluation_time=1.0):
    motor.pid.tunings = (kp, ki, kd)
    start_time = time.time()
    total_error = 0.0
    count = 0
    while time.time() - start_time < evaluation_time:
        error = abs(motor.pid.setpoint - motor.calculate_speed())
        total_error += error
        count += 1
    return total_error / count if count > 0 else 0.0


# Algoritmo Genético para ajuste de PID
def genetic_pid_tuning(motor, generations=10, population_size=6):
    """
    Ajusta os parâmetros PID do motor utilizando um Algoritmo Genético.
    :param motor: O motor a ser ajustado
    :param generations: Número de gerações do Algoritmo Genético
    :param population_size: Tamanho da população em cada geração
    """
    # Tenta carregar parâmetros salvos para o motor
    motor_name = motor.name
    loaded_params = load_pid_params(motor_name)
    
    # Verifica se os parâmetros carregados são os valores padrão (indicando que a otimização não foi feita)
    if loaded_params == (1.0, 0.1, 0.05):
        population = [
            (random.uniform(0.5, 2.0), random.uniform(0.01, 0.2), random.uniform(0.01, 0.1))
            for _ in range(population_size)
        ]

        for _ in range(generations):
            # Avalia a população e calcula o erro para cada conjunto de parâmetros
            fitness = [(kp, ki, kd, evaluate_pid(kp, ki, kd, motor)) for kp, ki, kd in population]
            fitness.sort(key=lambda x: x[3])  # Ordena pela menor quantidade de erro (fitness)

            # Seleciona os 3 melhores indivíduos
            best_individuals = fitness[:3]
            print(f"Melhor erro: {best_individuals[0][3]:.4f} | Kp={best_individuals[0][0]}, Ki={best_individuals[0][1]}, Kd={best_individuals[0][2]}")

            # Crossover - combina os melhores para criar novos indivíduos
            new_population = [
                (random.choice(best_individuals)[0], random.choice(best_individuals)[1], random.choice(best_individuals)[2])
                for _ in range(population_size - 2)
            ]

            # Mutação - pequena variação nos parâmetros
            new_population = [
                (kp * random.uniform(0.9, 1.1), ki * random.uniform(0.9, 1.1), kd * random.uniform(0.9, 1.1))
                for kp, ki, kd in new_population
            ]

            # Mantém os 2 melhores da geração anterior
            population = [(best_individuals[0][0], best_individuals[0][1], best_individuals[0][2]),
                        (best_individuals[1][0], best_individuals[1][1], best_individuals[1][2])] + new_population

        # Define os melhores parâmetros encontrados
        best_kp, best_ki, best_kd = best_individuals[0][:3]
        motor.pid.tunings = (best_kp, best_ki, best_kd)

        # Salva os melhores parâmetros no arquivo JSON
        save_pid_params(motor_name, best_kp, best_ki, best_kd)
    else:
        # Se os parâmetros carregados não forem padrão, usa-os diretamente
        motor.pid.tunings = loaded_params