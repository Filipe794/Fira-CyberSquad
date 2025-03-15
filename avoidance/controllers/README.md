# Controladores do Robô - Controllers

Este diretório contém os controladores do robô, responsáveis por gerenciar os sensores, motores, movimentação e outras funcionalidades. Abaixo está uma descrição de cada arquivo dentro da pasta `controllers`.

---

## `encoder_reader.py`

Este arquivo contém o código responsável pela leitura dos encoders, que são usados para calcular a velocidade e o deslocamento dos motores do robô. Ele configura os pinos dos encoders e implementa a lógica para contar os pulsos gerados pelos encoders.

### Funcionalidades:
- Inicializa o pino de leitura do encoder.
- Contabiliza os pulsos para calcular a velocidade do motor.
- Utiliza interrupções para ler os sinais do encoder de forma eficiente.

---

## `laser_sensor.py`

Este arquivo lida com o sensor de distância **TOF VL53L0X** para medir a distância até os obstáculos. Ele integra o sensor ao sistema do robô e fornece as leituras de distância em tempo real, usadas para a navegação e detecção de obstáculos.

### Funcionalidades:
- Configura o sensor TOF.
- Realiza leituras de distância e as retorna.
- Pode ser integrado ao algoritmo de evasão para evitar colisões.

---

## `motor_controller.py`

O arquivo `motor_controller.py` é responsável pelo controle dos motores do robô, implementando a lógica do **PID** (Proporcional, Integral e Derivativo) para regular a velocidade dos motores e manter a estabilidade durante a movimentação.

### Funcionalidades:
- Inicializa o PID para cada motor com parâmetros carregados (ou padrões).
- Controla o motor através de PWM (modulação por largura de pulso).
- Ajusta a direção e a velocidade do motor de acordo com a saída do PID.
- Usa interrupções para medir a velocidade com base nos encoders.

---

## `movement.py`

Este arquivo é responsável pelo controle de movimentação do robô, coordenando os motores e implementando a lógica para movimentação de acordo com os comandos recebidos.

### Funcionalidades:
- Gerencia o movimento do robô com base nos dados dos motores e sensores.
- Controla a velocidade e a direção com base nas leituras de PID.
- Lógicas de movimentação, como evasão de obstáculos.

---

## `pid_tuning.py`

Este arquivo implementa o **ajuste dinâmico dos parâmetros do PID** usando o algoritmo genético. O objetivo é encontrar os melhores valores de **Kp**, **Ki** e **Kd** para otimizar o controle dos motores, com base em uma função de erro calculada durante o movimento.

### Funcionalidades:
- Ajusta automaticamente os parâmetros do PID para melhorar o desempenho do robô.
- Implementa o algoritmo genético para otimizar os valores de PID.
- Carrega e salva os parâmetros de PID em um arquivo JSON para reutilização.

---

## `vision.py`

O arquivo `vision.py` integra a visão computacional ao robô, utilizando câmeras e algoritmos de processamento de imagem para detectar obstáculos ou objetos no ambiente. Ele pode ser usado para implementar sistemas como evasão de obstáculos baseados em visão, reconhecimento de objetos e até mesmo navegação autônoma.

### Funcionalidades:
- Lê e processa imagens da câmera.
- Aplica algoritmos de visão computacional para detectar obstáculos e objetos.
- Integra com o sistema de controle de movimentação para realizar evasão de obstáculos ou seguir trajetórias.

---

# Melhorias
    - Implementar LIDAR
    - Sensores VL53L0X
    - Testar implementações feitas
    - Lógica para desvio de obstáculos
    - Considerar usar ESP32 para aliviar o processamento do Raspberry, ja que talvez tenhamos apenas 2gb de ram