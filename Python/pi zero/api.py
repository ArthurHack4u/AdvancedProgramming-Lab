from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Variable global que actuará como caché para el último estado conocido del servo
servo_data = {
    "angulo": 0,
    "potentiometer_raw": 0,
    "duty_cycle_percent": 0.0,
    "estado": "inicializando",
    "ultima_actualizacion": datetime.now().isoformat()
}

@app.route("/")
def home():
    """
    Página principal que muestra los endpoints disponibles.
    """
    return jsonify({
        "mensaje": "API del Servomotor",
        "endpoints_disponibles": {
            "ver_datos (GET)": "/api/servo",
            "enviar_datos (POST)": "/api/servo/actualizar"
        }
    })

@app.route("/api/servo", methods=['GET'])
def get_servo_data():
    """
    Este endpoint GET permite a cualquiera (como un navegador web)
    consultar el último estado reportado por la Raspberry Pi.
    """
    return jsonify(servo_data)

@app.route("/api/servo/actualizar", methods=['POST'])
def update_servo_data():
    """
    Este endpoint POST es el que la Raspberry Pi usará para
    enviar sus datos. Recibe un JSON, actualiza el estado y responde.
    """
    global servo_data  # Indispensable para modificar la variable global

    try:
        # Obtener el JSON que envió la Pi
        data_recibida = request.json
        
        # Actualizar el diccionario 'servo_data' con los nuevos valores
        servo_data["angulo"] = data_recibida.get("angle_degrees")
        servo_data["potentiometer_raw"] = data_recibida.get("potentiometer_raw")
        servo_data["duty_cycle_percent"] = data_recibida.get("duty_cycle_percent")
        servo_data["estado"] = "activo"
        servo_data["ultima_actualizacion"] = datetime.now().isoformat()

        # Responder a la Pi que todo salió bien
        return jsonify({"status": "exito", "recibido": data_recibida}), 200

    except Exception as e:
        # Manejar errores (ej. si no se envió un JSON)
        return jsonify({"status": "error", "mensaje": str(e)}), 400

# ---- MAIN ----
if __name__ == "__main__":
    print("Iniciando servidor API en http://0.0.0.0:5000")
    print("Otros dispositivos en la red pueden conectarse a esta IP.")
    # host="0.0.0.0" hace que el servidor sea visible en tu red local
    app.run(host="0.0.0.0", port=5000)