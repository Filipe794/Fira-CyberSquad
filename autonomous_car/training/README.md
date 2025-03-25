
---

## **Estrutura do Projeto**

1. **Rede Neural com Imagens (Sem Detecção de Obstáculos)** - Utiliza apenas as imagens capturadas pela câmera para prever o ângulo do servo.
2. **Rede Neural com Imagens e Detecção de Obstáculos** - Combina as imagens da câmera com as distâncias medidas pelos sensores ToF (frontal e lateral direito) para prever o ângulo do servo.

## **1. Rede Neural com Imagens (Sem Detecção de Obstáculos)**

### **Arquitetura:**
- O modelo usa uma abordagem de **regressão** para prever o ângulo do servo motor (em graus), suavizando as curvas.

### **Modelo:**
A rede neural tem a seguinte estrutura:
- **Entrada:** Imagens de 128x128 pixels.
- **Camadas:** Baseadas no MobileNetV2 com uma camada de pooling global.
- **Saída:** Um único valor contínuo (ângulo do servo).

### **Como Treinar:**
- O dataset deve ser coletado com imagens e ângulos do servo, com o robô sendo controlado remotamente.

---

## **2. Rede Neural com Imagens e Detecção de Obstáculos**

### **Objetivo:**
A segunda versão da rede neural inclui **informações adicionais de distância** obtidas de **sensores ToF** (frontal e lateral direito). Essas informações ajudam a rede a ajustar a navegação do carro, levando em conta a presença de obstáculos e a necessidade de desviar para a esquerda, enquanto segue sempre pela via direita.

### **Arquitetura:**
- Adicionamos uma segunda entrada para as distâncias dos sensores ToF (dois sensores: frontal e lateral direito).
- A saída continua sendo um valor contínuo que representa o **ângulo do servo motor**.

### **Modelo:**
A rede neural tem as seguintes entradas:
- **Entrada de Imagem:** Imagens de 128x128 pixels (processadas pelo MobileNetV2).
- **Entrada de Distâncias:** Um vetor de 2 elementos representando as distâncias dos sensores ToF.
- **Camadas:** Camadas densas para combinar as distâncias com a saída da rede de imagens.
- **Saída:** Um valor contínuo (ângulo do servo).

---

## **Regressão na Rede Neural**

A rede neural usa **regressão** para prever o ângulo do servo motor. Isso significa que o modelo tenta prever um valor contínuo, em vez de classificar a direção como "esquerda", "direita" ou "reto". A regressão é uma abordagem ideal quando o objetivo é prever um valor contínuo como o **ângulo de rotação** do servo.

- **Função de Perda:** Utiliza o **Erro Quadrático Médio (MSE)** para minimizar a diferença entre o valor predito e o valor real do ângulo.
- **Métrica de Avaliação:** O **Erro Absoluto Médio (MAE)** é usado para avaliar a performance do modelo durante o treinamento.

---

## **Como Testar**

Para testar o modelo no ambiente real do carro autônomo, siga os seguintes passos:

1. **Carregar o Modelo**:
   - Para o modelo com **sensores de obstáculos**, carregue o modelo **TensorFlow Lite** (`servo_model_with_sensors.tflite`) no Raspberry Pi.
   - Para o modelo sem **sensores de obstáculos**, use o modelo original de regressão com imagens.

2. **Capturar Dados em Tempo Real**:
   - Use a câmera para capturar imagens da pista.
   - Obtenha as leituras dos sensores ToF (distância frontal e lateral) usando o código de captura.

3. **Prever o Ângulo**:
   - Passe as imagens e as distâncias pela rede neural para prever o **ângulo do servo motor**.
   - Ajuste o controle do servo motor com base no valor previsto.

4. **Testar em Ambiente Real**:
   - Coloque o carro na pista e verifique se ele consegue seguir a via corretamente.
   - Realize testes com obstáculos para ver como o carro reage à detecção e desvia conforme necessário.

---

## **Melhorias**

- **Performance:** O modelo pode ser otimizado utilizando diferentes redes neurais ou técnicas como **aumento de dados** (data augmentation).  
- **Ajustes de Hiperparâmetros:** Testar diferentes tamanhos de lotes (batch sizes) e épocas para melhorar a convergência.