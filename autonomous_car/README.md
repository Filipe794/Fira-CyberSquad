
---

### **1. Visão Geral do Projeto**
O objetivo é construir um carro autônomo em escala 1:10 que atenda às especificações da competição e seja capaz de competir nas duas modalidades:
- **Autonomous Race**: Completar voltas em uma pista com checkpoints e evitar obstáculos.
- **Autonomous Urban Driving**: Navegar em um ambiente urbano com sinais de trânsito, cruzamentos e obstáculos, seguindo regras específicas como parar em cruzamentos e manter-se na faixa correta.

#### **Requisitos Principais**
- **Dimensões**: Comprimento (300 mm a 550 mm), largura (150 mm a 350 mm), altura máxima (450 mm).
- **Rodas**: 4 rodas, tração 2WD (traseira).
- **Ambiente**: Pista de corrida com largura de 50 cm ± 10% e raio de curva mínimo de 1.5 m ± 10%; ambiente urbano com largura de 60 cm ± 10%, sinais de trânsito e April Tags.

---

### **2. Design Mecânico**
#### **2.1 Chassi**
- **Material**: Impressão 3D
- **Estrutura**: Chassi modular com compartimentos para bateria, Raspberry Pi, motores, sensores e microcontroladores.
- **Considerações**: Adicionar suportes elásticos (ex.: arruelas de borracha) entre os eixos e o chassi para absorver pequenas vibrações.

#### **2.2 Sistema de Direção**
- **Mecanismo**: Ackerman steering com servo motor.
- **Componentes**: Servo motor, braços de direção impressos em 3D
- 
#### **2.3 Bateria**
- **Tipo**: Bateria LiPo 2S (7.4V) ou 3S (11.1V)
- **Regulador**: Usar um regulador de tensão (ex.: módulo step-down) para fornecer 5V ao Raspberry Pi e outros componentes eletrônicos a partir da bateria LiPo.

---

### **3. Sistema Eletrônico**
#### **3.1 Unidade de Processamento**
- **Raspberry Pi**:
  - Visão computacional.
  - Navegação, Controle PID.
- **Arduino Nano**:
    - Controle dos Motores
    - Controle do Servo
    - Leitura de Sensores e envio de dados ao Raspberry Pi.

#### **3.2 Sensores**
- **Câmera**: Webcam USB
  - Posicionada na frente do carro, com ângulo ajustável para capturar a pista, sinais e April Tags.
- **Sensor para Obstáculos**: Sensor TOF VL53L0X.
  - Montado na frente do carro para detectar obstáculos a até 2 metros com alta precisão.
- **IMU**: MPU-6050 (acelerômetro + giroscópio).
  - Usado para medir orientação e aceleração, ajudando na navegação e estabilidade.
- **Encoder**: Encoders magnéticos ou ópticos acoplados aos motores N20 para feedback de velocidade e distância percorrida.
  - Alternativa: Se encoders específicos não estiverem disponíveis, usar sensores Hall simples com ímãs nas rodas traseiras.

#### **3.3 Comunicação**
- **Raspberry Pi <-> Arduino**: Comunicação serial (UART) entre o Raspberry Pi e os Arduinos Nano/Uno para troca de dados dos sensores e comandos para os motores.
- 
#### **3.4 Atuadores**
- **Servo Motor**: SG90 para o sistema de direção Ackerman.
  - Controlado diretamente pelo Raspberry Pi via GPIO (usando biblioteca como `RPi.GPIO`).
- **Motores N20**: Controlados pelo driver L298N, que será gerenciado pelo Arduino Nano.

---

### **4. Software**
#### **4.1 Sistema Operacional**
- **Sistema**: Raspbian OS no Raspberry Pi.
- **Bibliotecas**:
  - **OpenCV**: Para visão computacional (detecção de linhas, sinais, April Tags).
  - **RPi.GPIO**: Para controle do servo motor.
  - **PySerial**: Para comunicação serial entre Raspberry Pi e Arduinos.
  - **Adafruit_VL53L0X** (ou similar): Para leitura do sensor TOF no Arduino Uno.
  - **MPU6050** (biblioteca Arduino): Para leitura da IMU.

#### **4.2 Visão Computacional**
- **Detecção de Linhas**: Usar OpenCV para detectar as linhas contínuas e tracejadas (brancas ou pretas) da pista.
  - Algoritmo: Hough Transform para identificar bordas e calcular o centro da pista.
  - Ajustar parâmetros para lidar com variações de iluminação e cor.
- **Detecção de Sinais**: Implementar reconhecimento de April Tags com a biblioteca `apriltag` no OpenCV.
  - Para sinais de trânsito, usar aprendizado profundo (ex.: modelo YOLO leve treinado para os sinais mencionados).
- **Detecção de Obstáculos**: Processar imagens da câmera para identificar obstáculos e combinar com dados do sensor TOF.

#### **4.3 Navegação e Controle**
- **Path Planning**: Implementar um algoritmo simples (ex.: seguir linha com ajustes baseados em checkpoints) em Python no Raspberry Pi.
  - Para o modo urbano, usar uma tabela de decisão baseada nos sinais detectados (ex.: "Proceed Right" -> virar à direita).
- **Controle PID**: Implementar PID em Python no Raspberry Pi para:
  - Manter o carro no centro da pista (baseado na detecção de linhas).
  - Ajustar a velocidade dos motores N20 em curvas (controle diferencial).
- **Regras Específicas**:
  - Parar por 3 segundos antes de cruzamentos no modo urbano.
  - Manter-se na faixa correta ao passar por checkpoints.
  - Evitar obstáculos (combinar dados da câmera e TOF para desviar ou parar).

#### **4.4 Gerenciamento de Estados**
- **Máquina de Estados**: Implementar uma Finite State Machine em Python no Raspberry Pi para gerenciar diferentes modos:
  - **Seguir pista**: Autonomous Race (prioridade: seguir linhas, passar checkpoints).
  - **Modo urbano**: Parar em cruzamentos, interpretar sinais, seguir faixas.
  - **Reagir a obstáculos**: Desviar ou parar se detectar obstáculo próximo.

---

### Exemplos
https://www.youtube.com/watch?v=67Su8OhVuLs
https://pt.aliexpress.com/i/1005001962537643.html?gatewayAdapt=glo2bra
https://www.youtube.com/watch?v=xBFDSW4aEv0
https://www.youtube.com/watch?v=LzyIbJhcxhQ - direção paralela, mas serve de exemplo pra montagem
https://www.youtube.com/watch?v=ZvE6yuLVDVc - direção paralela, mas serve de exemplo pra montagem