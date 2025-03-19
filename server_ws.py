from flask import Flask
from flask_socketio import SocketIO, emit
import pickle

# Cargar el modelo y el vectorizador
with open("modelo.pkl", "rb") as model_file:
    modelo = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("mensaje")
def handle_message(data):
    mensaje = data.get("mensaje", "").strip()
    print(f"Mensaje recibido: {mensaje}")

    if not mensaje:
        emit("respuesta", {"respuesta": "❌ No entendí el mensaje. Intenta de nuevo."})
        return

    # 🔹 Convertir el mensaje en un vector numérico antes de predecir
    mensaje_vectorizado = vectorizer.transform([mensaje])

    # 🔹 Predecir la respuesta
    respuesta = modelo.predict(mensaje_vectorizado)[0]
    print(f"Respuesta enviada: {respuesta}")

    emit("respuesta", {"respuesta": respuesta})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
