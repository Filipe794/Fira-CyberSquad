# Interface de Debug para Monitoramento do Robô

Interface web para monitoramento em tempo real dos sensores e motores. Se conecta ao Raspberry Pi usando o Flask.

## Estrutura do Projeto

- **`main.py`**: Serve a aplicação Flask e envia dados para o front-end utilizando WebSockets.
- **`templates/index.html`**: Página HTML com os elementos de monitoramento do robô.
- **`static/script.js`**: Script que conecta a interface ao servidor Flask via WebSocket e atualiza os dados.
- **`static/styles.css`**: Estilos para a interface de usuário.

## Instruções
### 1. **Configuração do Raspberry Pi**

#### Passo 1: Instalar as dependências no Raspberry Pi

Instale as bibliotecas necessárias. Basta executar o arquivo requirements.txt

```pip install -r requirements.txt.```

#### Passo 2: Rodar o servidor Flask

Clone o repositório para o Raspberry Pi. Navegue até o diretório onde o arquivo `main.py` está localizado e execute o seguinte comando:

```bash
python3 main.py
```

### 2. **Configuração do PC para Acesso à Interface**

#### Passo 1: Descobrir o IP do Raspberry Pi

No Raspberry Pi, execute o seguinte comando para obter o IP da máquina:

```bash
hostname -I
```

Exemplo de saída:

```
192.168.1.100
```

Este será o IP do Raspberry Pi, que você usará para acessar a interface no PC.

#### Passo 2: Alterar o Script JavaScript

No arquivo `static/script.js`, altere a linha de conexão do WebSocket para usar o IP do Raspberry Pi, como mostrado abaixo:

```
var socket = io.connect('http://192.168.1.100:5000');  // Use o IP do Raspberry Pi
```

### 3. **Acessando a Interface no Navegador**

No PC, abra um navegador de internet e digite o seguinte URL:

```
http://192.168.1.100:5000
```

Substitua `192.168.1.100` pelo IP do Raspberry Pi. Isso deve carregar a página com os dados do robô sendo atualizados em tempo real.

### 4. **Monitoramento em Tempo Real**

Os seguintes dados são monitorados e exibidos na interface:

- **Velocidade dos Motores**: Velocidades em RPM dos motores.
- **Distâncias dos Sensores ToF**: Distâncias dos sensores ToF (frontal, esquerdo e direito) em centímetros.
- **Parâmetros PID**: Valores de Kp, Ki e Kd de cada motor.

### 5. **Solucionando Problemas Comuns**

- **Conexão recusada**:
    - Verifique se o Raspberry Pi e o PC estão na mesma rede local.
    - Certifique-se de que o servidor Flask está rodando no Raspberry Pi.
    - Verifique se a porta 5000 está liberada no firewall do Raspberry Pi.

- **Página não carrega ou WebSocket não conecta**:
    - Certifique-se de que o IP do Raspberry Pi foi corretamente configurado no arquivo `script.js`.
    - Tente acessar o Raspberry Pi de outra máquina na mesma rede para verificar se o problema é na rede.