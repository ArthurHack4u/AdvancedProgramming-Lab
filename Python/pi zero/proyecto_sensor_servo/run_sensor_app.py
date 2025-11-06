"""
Punto de entrada para el SENSOR (Potenciómetro).
Este script lee el potenciómetro y envía los datos a la API.
Reemplaza la lógica de 'pizero.py'.
"""
import RPi.GPIO as GPIO
import time
from src.hardware.potentiometer import Potentiometer
from src.client.api_client import SensorAPIClient

# --- CONFIGURACIÓN ---
# ¡¡¡IMPORTANTE!!! CAMBIA ESTA IP
API_BASE_URL = "http://192.168.1.133:5000" 
POT_PIN = 4  # Pin BCM del potenciómetro
UPDATE_INTERVAL = 1.0  # Segundos entre envíos a la API

def main():
    print("Iniciando aplicación SENSOR...")
    
    # Inicializar GPIO
    GPIO.setmode(GPIO.BCM)
    
    # Inicializar módulos
    pot = Potentiometer(POT_PIN)
    client = SensorAPIClient(API_BASE_URL)
    
    # Calibrar
    min_val, max_val = pot.calibrate()
    
    print("\nEnviando datos del potenciómetro a la API...")
    
    while True:
        # Leer valor normalizado (0.0 a 1.0)
        normalized_value = pot.get_normalized_value()
        
        # Convertir a ángulo y duty cycle
        angle = normalized_value * 180
        duty_cycle = (angle / 18) + 2.5
        
        # Leer valor crudo (para el payload)
        raw_val = pot.read_raw_value()
        
        # Enviar a la API
        client.update_servo_data(
            pot_raw=raw_val,
            angle=angle,
            duty_cycle=duty_cycle
        )
        
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma detenido.")
    finally:
        print("Limpiando pines GPIO...")
        GPIO.cleanup()
