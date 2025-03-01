## Deteção de Obstáculos
1. Pré-processamento da imagem: mudança de cor, blurr, threshold
2. Detecção de bordas
3. Segmentação de obstáculos
4. Redes Neurais: se o processamento apenas com OpenCV não der conta, utilizar um modelo leve (MobileNetSSD)

## Planejamento de Caminho
1. Algoritmo de Path Planning (A*, Dijkstra, RRT):  adicionar peso para células mt próximas de obstaculos para evitar colisão
2. Implementação Pure Pursuit: facilita seguir trajetórias de forma suave
3. Validar distâncias com o sensor laser ou LIDAR

## Execução 
1. Utilizar Threads para rodar visão + sensores em paralelo
2. Otimizações com OpenCV (GStreamer, MMAL) e numpy

## Montagem
1. Câmera levemente apontada para o chão (~30º-45º): cobre melhor o caminho livre e obstáculos a frente, os sensores a laser ficarão responsáveis por medir a distância exata dos obstáculos.
2. Se a câmera estiver montada entre 15 e 30cm acima do robo, facilitaria o path planning, uma vez que a imagem seria mais algo semelhante a um mapa 2D.

## Testes
1. Testar o campo de visão da camera com um algoritmo simples
2. Se necessário, aplicar uma transformação de perspectiva (Bird's Eye View)
3. Gerar uma mapa de ocupação inicial

## Estratégia Final
1. Definir um waypoint inicial e um objetivo final no lado oposto.
2. Usar A* ou RRT* para planejar o caminho com zonas de segurança.
3. Recalcular a rota sempre que um novo obstáculo for detectado.
4. Armazenar dados dos testes para melhorar a estratégia com aprendizado supervisionado.
5. Testar aprendizado por reforço se for necessário um comportamento mais adaptável.


## Links
https://www.youtube.com/watch?v=G9Yp8S7TT04 - https://github.com/adi932001/OpenCV-Projects

grade de ocupação com pesos

waypoints inicial e final

a* ou rrt*

pure pursuit