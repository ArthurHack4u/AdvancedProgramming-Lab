"""
Este archivo no contiene código ejecutable, sino que define la "forma"
(esquema) de los datos JSON que la API espera y devuelve.
Sirve como documentación centralizada para los datos.
"""

# Este es el objeto que se almacena en el caché del servidor
# y se devuelve en el endpoint GET /api/servo
SERVO_DATA_SCHEMA = {
    "angulo": 0,
    "potentiometer_raw": 0,
    "duty_cycle_percent": 0.0,
    "estado": "inicializando | activo",
    "ultima_actualizacion": "2023-10-27T10:00:00.000000"
}

# Este es el objeto que el cliente (la Pi con sensor)
# debe enviar en el endpoint POST /api/servo/actualizar
POST_PAYLOAD_SCHEMA = {
    "potentiometer_raw": 12345,
    "angle_degrees": 90.5,
    "duty_cycle_percent": 7.5
}
