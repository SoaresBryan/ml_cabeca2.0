from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2
import mediapipe as mp
import threading
import pyautogui  # Importa o pyautogui para simular pressionamento de teclas
import utils.detector as detector
import utils.treinamento as treinamento

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
socketio = SocketIO(app, cors_allowed_origins="*")

# Variáveis globais para controle
coletando_dados = False
label_atual = None
ultima_direcao = None

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('start_collection')
def handle_start_collection(data):
    global coletando_dados, label_atual
    coletando_dados = True
    label_atual = data['label']
    print(f"Iniciando coleta para o movimento: {label_atual}")

@socketio.on('stop_collection')
def handle_stop_collection():
    global coletando_dados, label_atual
    coletando_dados = False
    label_atual = None
    print("Coleta de dados finalizada.")
    treinamento.salvar_dados()

@socketio.on('train_model')
def handle_train_model():
    print("Iniciando treinamento do modelo...")
    treinamento.treinar_modelo()
    print("Modelo treinado com sucesso.")
    emit('status', {'message': 'Modelo treinado com sucesso.'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed_route():
    return Response(generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def acionar_tecla(direcao):
    """Função para acionar a tecla correspondente à direção detectada."""
    if direcao == "up":
        pyautogui.press("up")
    elif direcao == "down":
        pyautogui.press("down")
    elif direcao == "left":
        pyautogui.press("left")
    elif direcao == "right":
        pyautogui.press("right")

def generate_video_feed():
    global ultima_direcao
    cap = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                features = detector.extract_features(face_landmarks)
                
                if coletando_dados and label_atual:
                    treinamento.coletar_dados(features, label_atual)
                elif treinamento.modelo_treinado:
                    direction = treinamento.modelo.predict([features])[0]
                    
                    # Emite o comando da direção para o front-end
                    socketio.emit('command', {'direction': direction})
                    
                    # Executa o comando de tecla apenas se a direção mudou
                    if direction != ultima_direcao:
                        acionar_tecla(direction)
                        ultima_direcao = direction

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
