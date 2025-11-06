# API del Servomotor

Esta API actúa como un puente de comunicación (un "caché" en memoria) entre un dispositivo sensor (potenciómetro) y un dispositivo actuador (servo).

El objetivo es desacoplar los sistemas: el sensor solo se preocupa de *reportar* su estado, y el actuador solo se preocupa de *leer* el último estado deseado.

## Endpoints

### 1. Obtener Estado del Servo

Permite a cualquier cliente (como el script del actuador `run_actuator_app.py`) consultar el último estado reportado por el sensor.

* **URL:** `/api/servo`

* **Método:** `GET`

* **Respuesta Exitosa (Código 200):**

{ "angulo": 90.5, "potentiometer_raw": 12345, "duty_cycle_percent": 7.5, "estado": "activo", "ultima_actualizacion": "2023-10-27T10:01:00.123456" }
* **Respuesta si está inicializando (Código 200):**

{ "angulo": 0, "potentiometer_raw": 0, "duty_cycle_percent": 0.0, "estado": "inicializando", "ultima_actualizacion": "2023-10-27T10:00:00.000000" }

### 2. Actualizar Estado del Servo

Usado por el dispositivo sensor (el script `run_sensor_app.py`) para reportar nuevos datos al servidor.

* **URL:** `/api/servo/actualizar`

* **Método:** `POST`

* **Payload (JSON Requerido):**

* Este es el JSON que el cliente debe enviar en el cuerpo (body) de la petición.

{ "potentiometer_raw": 12345, "angle_degrees": 90.5, "duty_cycle_percent": 7.5 }

* **Respuesta Exitosa (Código 200):**

* Confirma que los datos fueron recibidos y procesados.

{"status": "exito", "recibido": { "potentiometer_raw": 12345, "angle_degrees": 90.5, "duty_cycle_percent": 7.5 } }

* **Respuesta de Error (Código 400):**

* Ocurre si el JSON está malformado o faltan campos clave.

{ "status": "error", "mensaje": "Faltan datos en el JSON (angle_degrees, potentiometer_raw)" }