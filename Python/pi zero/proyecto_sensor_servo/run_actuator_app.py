"""
Punto de entrada para el ACTUADOR (Servo).
Este script lee el estado de la API y mueve el servo.
Cumple con la Tarea 4: "Utilizar los datos de la API para controlar un servo".
"""
import RPi.GPIO as GPIO
import time
from src.hardware.servo import Servo
from src.client.api_client import SensorAPIClient

# --- CONFIGURACIÓN ---
# ¡¡¡IMPORTANTE!!! CAMBIA ESTA IP
API_BASE_URL = "http://192.168.1.133:5000" 
SERVO_PIN = 18  # Pin BCM del servo
POLL_INTERVAL = 0.5  # Segundos entre lecturas de la API

def main():
    print("Iniciando aplicación ACTUADOR...")
    
    # Inicializar GPIO
    GPIO.setmode(GPIO.BCM)
    
    # Inicializar módulos
    servo = Servo(SERVO_PIN)
    client = SensorAPIClient(API_BASE_URL)
    
    print("\nLeyendo de la API y controlando el servo...")
    
    last_known_angle = -1 # Para evitar mover el servo innecesariamente

    while True:
        # Obtener datos de la API
        data = client.get_servo_data()
        
        if data and "angulo" in data:
            angle_from_api = data["angulo"]
            
            # Solo mover si el ángulo ha cambiado
            if angle_from_api != last_known_angle:
                servo.set_angle(angle_from_api)
                last_known_angle = angle_from_api
            else:
                print(f"[Servo] Ángulo sin cambios ({angle_from_api:.1f}°).")
                
        else:
            print("[Servo] No se pudieron obtener datos de la API.")
            
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma detenido.")
    finally:
        print("Limpiando pines GPIO...")
        # El 'servo.stop()' se podría llamar aquí si se instancia 'servo' fuera de main
        # Pero GPIO.cleanup() detendrá el PWM de todas formas.
        GPIO.cleanup()
