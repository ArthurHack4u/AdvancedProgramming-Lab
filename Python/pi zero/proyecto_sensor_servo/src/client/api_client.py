import requests
import time

class SensorAPIClient:
    """
    Cliente para consumir la API del sensor/servo.
    Implementa Tarea 3: Cliente de API y manejo de errores.
    """
    def __init__(self, base_url, retries=3, delay=2):
        """
        Inicializa el cliente de la API.
        :param base_url: La URL base del servidor (ej: "http://192.168.1.133:5000")
        :param retries: Número de reintentos en caso de fallo (Tarea 3).
        :param delay: Segundos de espera entre reintentos.
        """
        self.base_url = base_url
        self.api_url_get = f"{base_url}/api/servo"
        self.api_url_update = f"{base_url}/api/servo/actualizar"
        self.retries = retries
        self.delay = delay
        print(f"[Cliente API] Conectando a: {self.base_url}")

    def _request_with_retry(self, method, url, **kwargs):
        """
        Método interno para manejar reintentos en las peticiones.
        """
        for attempt in range(self.retries):
            try:
                # Timeout de 0.5s para no bloquear el script
                response = requests.request(method, url, timeout=0.5, **kwargs)
                response.raise_for_status()  # Lanza error si es 4xx o 5xx
                return response
            except requests.exceptions.RequestException as e:
                print(f"[Cliente API] Error: {e}. Intento {attempt + 1}/{self.retries}.")
                time.sleep(self.delay)
        
        print(f"[Cliente API] Fallo al conectar con {url} después de {self.retries} intentos.")
        return None

    def get_servo_data(self):
        """
        Obtiene los últimos datos del servo desde la API.
        :return: Un diccionario con los datos o None si falla.
        """
        print("[Cliente API] Solicitando datos (GET)...")
        response = self._request_with_retry('GET', self.api_url_get)
        if response:
            return response.json()
        return None

    def update_servo_data(self, pot_raw, angle, duty_cycle):
        """
        Envía (POST) los nuevos datos del sensor a la API.
        :param pot_raw: Valor crudo del potenciómetro.
        :param angle: Ángulo calculado.
        :param duty_cycle: Ciclo de trabajo calculado.
        :return: True si fue exitoso, False si falló.
        """
        payload = {
            "potentiometer_raw": pot_raw,
            "angle_degrees": round(angle, 2),
            "duty_cycle_percent": round(duty_cycle, 2)
        }
        print(f"[Cliente API] Enviando datos (POST): Ángulo={angle:.1f}")
        response = self._request_with_retry('POST', self.api_url_update, json=payload)
        
        if response:
            print("[Cliente API] Datos enviados con éxito.")
            return True
        return False