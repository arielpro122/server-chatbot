'''
from flask import Flask
from flask_socketio import SocketIO, emit
import pickle
import traceback
import datetime
import os

# Cargar el modelo y el vectorizador
try:
    with open("modelo.pkl", "rb") as model_file:
        modelo = pickle.load(model_file)

    with open("vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    modelo_cargado = True
except Exception as e:
    modelo_cargado = False
    with open("errores.log", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} ❌ Error cargando el modelo: {e}\n")

# Respuestas de respaldo (fallback)
respuestas_fallback = [
    "📄 Puedes consultar la guía oficial de servicio social aquí: [enlace]",
    "ℹ️ Si tienes dudas, visita el portal de servicio social de la UDG.",
    "🛠️ Estamos teniendo problemas técnicos. Intenta más tarde, por favor."
]

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("mensaje")
def handle_message(data):
    mensaje = data.get("mensaje", "").strip()
    print(f"📥 Mensaje recibido: {mensaje}")

    if not mensaje:
        emit("respuesta", {"respuesta": "❌ No entendí el mensaje. Intenta de nuevo."})
        return

    if not modelo_cargado:
        respuesta = respuestas_fallback[0]
        emit("respuesta", {"respuesta": respuesta})
        return

    try:
        mensaje_vectorizado = vectorizer.transform([mensaje])
        respuesta = modelo.predict(mensaje_vectorizado)[0]
        print(f"📤 Respuesta enviada: {respuesta}")
        emit("respuesta", {"respuesta": respuesta})

    except Exception as e:
        print("⚠️ Error en la predicción:")
        traceback.print_exc()

        # Guardar error en log
        with open("errores.log", "a") as log_file:
            log_file.write(f"{datetime.datetime.now()} ⚠️ Error procesando mensaje: {e}\n")

        # Enviar respuesta de respaldo
        fallback = respuestas_fallback[1]
        emit("respuesta", {"respuesta": fallback})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
'''











from flask import Flask
from flask_socketio import SocketIO, emit
import pickle

#Cargar el modelo y el vectorizador
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

     #🔹 Convertir el mensaje en un vector numérico antes de predecir
    mensaje_vectorizado = vectorizer.transform([mensaje])

     #🔹 Predecir la respuesta
    respuesta = modelo.predict(mensaje_vectorizado)[0]
    print(f"Respuesta enviada: {respuesta}")

    emit("respuesta", {"respuesta": respuesta})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)




