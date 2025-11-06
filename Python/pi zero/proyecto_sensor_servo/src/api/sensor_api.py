from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Variable global que actúa como caché para el último estado conocido.
# Esto simula una pequeña base de datos en memoria.
servo_data_cache = {
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
    Endpoint GET para consultar el último estado conocido del servo.
    Cualquier cliente (como la app del actuador) puede leer de aquí.
    """
    return jsonify(servo_data_cache)

@app.route("/api/servo/actualizar", methods=['POST'])
def update_servo_data():
    """
    Endpoint POST para que la Pi con el sensor (potenciómetro)
    envíe los nuevos datos. Recibe un JSON y actualiza el caché.
    """
    global servo_data_cache

    try:
        data_recibida = request.json
        
        # Validar que los datos necesarios están presentes (opcional pero recomendado)
        if "angle_degrees" not in data_recibida or "potentiometer_raw" not in data_recibida:
            raise ValueError("Faltan datos en el JSON (angle_degrees, potentiometer_raw)")

        # Actualizar el diccionario 'servo_data_cache' con los nuevos valores
        servo_data_cache["angulo"] = data_recibida.get("angle_degrees")
        servo_data_cache["potentiometer_raw"] = data_recibida.get("potentiometer_raw")
        servo_data_cache["duty_cycle_percent"] = data_recibida.get("duty_cycle_percent", 0.0)
        servo_data_cache["estado"] = "activo"
        servo_data_cache["ultima_actualizacion"] = datetime.now().isoformat()

        return jsonify({"status": "exito", "recibido": data_recibida}), 200

    except Exception as e:
        # Manejar errores (ej. si no se envió un JSON o faltan datos)
        return jsonify({"status": "error", "mensaje": str(e)}), 400

# ---- MAIN ----
if __name__ == "__main__":
    print("Iniciando servidor API en http://0.0.0.0:5000")
    print("Otros dispositivos en la red pueden conectarse a esta IP.")
    # host="0.0.0.0" hace que el servidor sea visible en tu red local
    app.run(host="0.0.0.0", port=5000, debug=True)
