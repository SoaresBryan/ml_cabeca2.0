

# Projeto de Controle de Setas com Movimentos Faciais

Este projeto utiliza Python, Flask, OpenCV e Machine Learning para permitir o controle de comandos de setas (cima, baixo, esquerda e direita) a partir dos movimentos da cabeça detectados pela webcam. Com o uso de uma câmera, o sistema detecta e classifica os movimentos faciais e emite comandos de tecla de seta correspondentes, usando a biblioteca `pyautogui` para simular o pressionamento das teclas, você pode testar nesse joguinho: https://snakegame.gg/pt/ :D.

## Funcionalidades

- **Detecção de Movimentos Faciais**: Utiliza MediaPipe e OpenCV para detectar pontos faciais e rastrear movimentos.
- **Treinamento de Modelo de Machine Learning**: Permite coletar dados de movimentos específicos e treinar um modelo de SVM para reconhecer esses movimentos.
- **Simulação de Teclas**: Usa `pyautogui` para simular pressionamentos das teclas de seta com base nos movimentos detectados.

## Tecnologias Utilizadas

- Python 3
- Flask
- Flask-SocketIO
- OpenCV
- MediaPipe
- scikit-learn
- pyautogui

## Pré-requisitos

- Python 3 instalado
- Webcam funcionando

### Instalação das Dependências

Instale as dependências com o seguinte comando:

```bash
pip install -r requirements.txt
```

## Como Usar

1. **Inicialize o Servidor**: Execute o servidor Flask com o seguinte comando:

   ```bash
   python app.py
   ```

2. **Acesse a Interface Web**: Abra o navegador e vá para `http://localhost:5000`. Você verá a interface com o vídeo da webcam e os controles para coleta de dados e treinamento.

3. **Coletar Dados para Treinamento**:

   - Na interface, você verá botões de coleta para movimentos específicos (Cima, Baixo, Esquerda e Direita).
   - Clique no botão correspondente ao movimento desejado e execute o movimento com a cabeça. O sistema coletará os dados por 5 segundos e os armazenará.
   - Repita o processo para cada movimento desejado para garantir que o modelo receba dados suficientes para cada direção.

4. **Treinar o Modelo**:

   - Após coletar dados para todos os movimentos, clique em "Treinar Modelo" na interface.
   - O sistema usará os dados coletados para treinar um modelo de SVM e salvará o modelo em `models/modelo_movimentos.pkl`.

5. **Usar os Comandos de Seta com Movimentos Faciais**:

   - Com o modelo treinado, mova a cabeça conforme os movimentos configurados (cima, baixo, esquerda, direita).
   - O sistema detectará os movimentos e enviará os comandos de seta para o computador, simulando pressionamentos de tecla correspondentes.


