# FIRA Avoidance

# GOOGLE COLAB
Processo de construção do prototipo descrito, ideias, métodos, equipamentos, entre outras coisas.
[FIRA RoboWorld Cup 2025 - RoboSot Avoidance](https://colab.research.google.com/drive/1zOWoBk5XVAWFry4xdbjDOlhXJQDDv-WG?usp=sharing)

## Sugestão 
As implementações, melhorias e observações estão marcadas com comentários "TODO". Para ficar mais fácil de encontrá-los estou utilizando a extensão do VsCode - Todo Tree.

## Arquivos Principais

### `config.py`
O arquivo `config.py` contém todas as configurações globais do projeto. Aqui são definidos os pinos GPIO utilizados para os motores, sensores, limites de PWM, intervalos de atualização do PID e o nome do arquivo de configuração do PID. Serve como ponto central para modificar qualquer configuração do hardware ou parâmetros que podem ser necessários.

### `main.py`
O arquivo `main.py` é o ponto de entrada do projeto. Ele integra todos os componentes do robô.

### `requirements.txt`
O arquivo `requirements.txt` contém uma lista de todas as bibliotecas e dependências necessárias para rodar o projeto. Ele facilita a instalação rápida das bibliotecas necessárias utilizando o comando `pip install -r requirements.txt`.


## Path Planning

Sugestão de Path Planning: Mapas de ocupação gerados pela visão computacional. Células com valor `0` indicam áreas livre e as células com valor `1 ` indicam obstáculos.

### Algoritmos Utilizados:
#### **A\*** (A-star):
- O algoritmo A* encontra o caminho mais curto entre dois pontos, utilizando uma função de custo `f(n) = g(n) + h(n)`, onde `g(n)` é o custo do caminho até o nó e `h(n)` é uma estimativa da distância até o objetivo. Ele é eficiente para ambientes conhecidos e mapeados.

#### **RRT (Rapidly-exploring Random Tree)**: 
- O algoritmo RRT é ideal para ambientes dinâmicos e de alta dimensão. Ele constrói uma árvore de busca de forma aleatória, explorando rapidamente o espaço de configurações e tentando encontrar um caminho entre o ponto inicial e o ponto de destino.

#### **Pure Pursuit**:
- O controlador Pure Pursuit é usado para o robô seguir o caminho gerado de maneira eficiente. O algoritmo calcula o ponto de referência mais próximo no caminho e ajusta a direção do robô para alcançá-lo de forma suave e contínua. Ele é adequado para trajetórias curvas e fornece controle de navegação eficiente em ambientes reais.

- Referências: https://www.mathworks.com/help/nav/ug/pure-pursuit-controller.html

### Custos das Células:
- Para evitar que o robô passe muito perto das bordas ou de áreas com alta densidade de obstáculos, as células próximas às bordas do mapa possuem um custo maior. Isso garante que o robô prefira caminhos mais centrais e distantes de áreas de risco.

### Como Funciona:
1. **Detecção de Obstáculos:** A câmera ou os sensores de proximidade do robô coletam informações sobre o ambiente.
2. **Geração do Mapa de Ocupação:** O ambiente é mapeado em um grid, onde cada célula é classificada como livre ou ocupada.
3. **Planejamento de Caminho:** O algoritmo A* ou RRT é usado para gerar um caminho seguro até o destino, considerando obstáculos e a configuração do robô.
4. **Execução do Caminho:** O robô segue o caminho gerado usando o controle de Pure Pursuit, ajustando sua trajetória conforme necessário.

## Dependências:
- Visão computacional para mapeamento do ambiente.
- Algoritmos A* ou RRT para geração do caminho.
- Algoritmo de controle Pure Pursuit para navegação do robô.
