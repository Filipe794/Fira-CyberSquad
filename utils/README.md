# Utilitários do Projeto - Pasta `utils`

A pasta `utils` contém arquivos que fornecem funcionalidades auxiliares para o funcionamento do robô.

## 1. `pid_manager.py`

O arquivo `pid_manager.py` é responsável por carregar, salvar e atualizar os parâmetros do controlador PID dos motores, permitindo que esses parâmetros sejam ajustados dinamicamente durante o funcionamento do robô. Além disso, ele também garante que os parâmetros sejam persistidos entre as execuções do robô por meio de um arquivo JSON.