
---

### TODO - Lista de Tarefas Pendentes para o Projeto do Robô

#### 1. Lógica Principal e Integração
- [ ] **Implementar lógica principal do robô** (`main.py`):
  - Definir o fluxo principal que integra sensores, visão, controle de motores e path planning.
  - Exemplo: loop principal que lê sensores, processa visão e ajusta movimentação.
- [ ] **Implementar lógica de movimentação baseada na detecção de obstáculos (Visão e Sensores VL53L0X)** (`movement.py` / `set_robot_velocity_with_vision`):
  - Ajustar velocidades (`vx`, `vy`, `omega`) com base em posições de obstáculos da visão e leituras do VL53L0X.
  - Exemplo: desacelerar ou girar quando obstáculos estão próximos (< 200mm).

#### 2. Tratamento de Falhas e Robustez
- [ ] **Lidar com falha de sensores** (`main.py`):
  - Implementar detecção de falhas (ex.: leituras inválidas do VL53L0X ou encoders) e fallback (ex.: parar motores ou usar valores estimados).
  - Exemplo: verificar se `distance_sensor.get_distance()` retorna valores fora do esperado.
- [ ] **Adicionar sincronização para acesso ao arquivo JSON** (`pid_manager.py`):
  - Usar `threading.Lock` em `load_pid_params` e `save_pid_params` para evitar corrupção em cenários multi-threaded.
- [ ] **Implementar restauração automática do backup** (`pid_manager.py`):
  - Se a escrita em `PID_CONFIG_FILE` falhar, restaurar o arquivo `.bak` original.

#### 3. Sensores e Hardware
- [ ] **Adicionar suporte aos sensores laterais VL53L0X** (`laser_sensor.py`):
  - Configurar múltiplos sensores (ex.: frente, esquerda, direita) via I2C com endereços distintos.
  - Integrar leituras laterais na lógica de movimentação.
- [ ] **Implementar LIDAR** (`controllers`):
  - Substituir ou complementar o VL53L0X com um LIDAR para mapeamento mais preciso.
  - Atualizar `vision.py` ou criar novo módulo para processar dados do LIDAR.
- [ ] **Monitorar a carga da bateria** (`main.py`):
  - Adicionar sensor de tensão/carga (ex.: via ADC) e lógica para alertar ou parar o robô se a bateria estiver baixa.
- [ ] **Considerar usar ESP32 para aliviar o processamento do Raspberry Pi** (`controllers`):
  - Delegar controle de motores e leitura de sensores ao ESP32, deixando o Raspberry para visão e path planning.
  - Implementar comunicação (ex.: UART ou I2C) entre os dispositivos.

#### 4. Controle e Movimentação
- [ ] **Implementar um filtro melhor para a leitura do encoder, se necessário** (`encoder_reader.py`):
  - Substituir média móvel por filtro mais avançado (ex.: Kalman) para suavizar ruídos nas leituras de velocidade.
- [ ] **Testar implementações feitas** (`controllers`):
  - Validar funcionamento de `motor_controller.py`, `encoder_reader.py`, e integração com sensores em cenários reais.
- [ ] **Lógica para desvio de obstáculos** (`movement.py` / `controllers`):
  - Combinar dados de visão e VL53L0X com algoritmos como A*, RRT ou Pure Pursuit para desviar de obstáculos dinamicamente.
  - Exemplo: reduzir `vx` e ajustar `omega` para contornar obstáculos detectados.

#### 5. Interface e Visualização
- [ ] **Interface de controle e visualização de dados em tempo real** (`main.py`):
  - Criar interface (web sugerida) para monitoramento de sensores, velocidades e mapa de ocupação.
  - Exemplo: usar Flask ou FastAPI com WebSocket para exibir dados em um navegador.

#### 6. Otimização e Ajustes
- [ ] **Aprimorar validação de parâmetros PID** (`pid_manager.py`):
  - Adicionar limites superiores realistas (ex.: Kp < 10.0) baseados no hardware em `update_pid_parameters`.
- [ ] **Integrar algoritmos de Path Planning** (`movement.py` / `vision.py`):
  - Implementar A* ou RRT para gerar caminhos em mapas de ocupação.
  - Usar Pure Pursuit para seguir os caminhos gerados com suavidade.

#### 7. Documentação e Testes
- [ ] **Documentar uso de novos componentes**:
  - Atualizar documentação para incluir LIDAR, ESP32 ou interface web, se implementados.
- [ ] **Criar testes unitários**:
  - Testar `pid_manager.py` (carregamento/salvamento), `encoder_reader.py` (velocidade), e `motor_controller.py` (PID).

---