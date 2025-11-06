import RPi.GPIO as GPIO
import time
import requests # <--- Necesario para hablar con la API

# -----------------------------------------------------------------
# ¡¡¡IMPORTANTE!!!
# CAMBIA ESTA IP por la IP de la PC donde corre el 'api_server.py'
# -----------------------------------------------------------------
API_ENDPOINT_URL = "http://192.168.1.133:5000/api/servo/actualizar"

# Cada cuántos segundos enviar datos a la API (para no saturarla)
API_UPDATE_INTERVAL = 1.0  # 1 segundo

# --- Configuración de Pines ---
POT_PIN = 4
SERVO_PIN = 18
FREQUENCY = 50

# --- Inicialización de GPIO ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# --- Configuración del PWM para el Servo ---
pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
pwm.start(2.5)  # Empezamos en 0 grados

def read_potentiometer():
    """
    Lee el valor del potenciómetro midiendo el tiempo de carga de un capacitor.
    """
    count = 0
    GPIO.setup(POT_PIN, GPIO.OUT)
    GPIO.output(POT_PIN, GPIO.LOW)
    time.sleep(0.01)
    
    GPIO.setup(POT_PIN, GPIO.IN)
    while GPIO.input(POT_PIN) == GPIO.LOW:
        count += 1
        if count > 100000: # Timeout
            break 
    return count

def calibrate():
    """
    Función interactiva para calibrar los valores mínimo y máximo del potenciómetro.
    """
    print("Iniciando calibración...")
    input("Gira el potenciómetro completamente a la izquierda (0 grados) y presiona Enter.")
    min_val = read_potentiometer()
    print(f"Valor mínimo registrado: {min_val}")
    
    print("-" * 20)
    
    input("Ahora, gira el potenciómetro completamente a la derecha (180 grados) y presiona Enter.")
    max_vals = [read_potentiometer() for _ in range(3)]
    max_val = max(max_vals)
    print(f"Valor máximo registrado: {max_val}")
    
    print("-" * 20)
    print("¡Calibración completada!")
    
    if max_val <= min_val:
        print("Advertencia: El valor máximo y mínimo son iguales. Asignando rango por defecto.")
        max_val = min_val + 100 

    return min_val, max_val

try:
    min_value, max_value = calibrate()
    
    print("\nControlando el servo con el potenciómetro... (Presiona Ctrl+C para detener)")
    
    # Variable para controlar el tiempo de envío a la API
    last_api_send_time = time.time()
    
    while True:
        # --- 1. Control del Servo (se ejecuta en cada ciclo) ---
        pot_value = read_potentiometer()
        
        # Normalizar el valor: 0.0 a 1.0
        normalized_value = (pot_value - min_value) / (max_value - min_value)
        normalized_value = max(0.0, min(1.0, normalized_value))
        
        # Convertir a ángulo: 0 a 180
        angle = normalized_value * 180
        
        # Convertir a ciclo de trabajo (duty cycle)
        duty_cycle = (angle / 18) + 2.5
        
        # Mover el servo
        pwm.ChangeDutyCycle(duty_cycle)
        
        # Imprimir el estado localmente
        print(f"Valor Pot: {pot_value:5d} -> Ángulo: {angle:5.1f}° -> Duty Cycle: {duty_cycle:4.1f}%")
        
        
        # --- 2. Envío a la API (se ejecuta 1 vez por segundo) ---
        current_time = time.time()
        if (current_time - last_api_send_time) > API_UPDATE_INTERVAL:
            
            # Preparamos los datos
            data_to_send = {
                "potentiometer_raw": pot_value,
                "angle_degrees": round(angle, 2),
                "duty_cycle_percent": round(duty_cycle, 2)
            }
            
            # Intentamos enviar (sin bloquear el script)
            try:
                # 'timeout=0.5' evita que el script se congele si la API está lenta
                requests.post(API_ENDPOINT_URL, json=data_to_send, timeout=0.5) 
                print(">>> Datos enviados a la API con éxito.")
                last_api_send_time = current_time # Reseteamos el contador
                
            except requests.exceptions.RequestException as e:
                # Si falla (API caída, sin WiFi), solo imprimimos el error
                # y el script del servo continúa funcionando.
                print(f"!!! Error de conexión con la API: {e}")
        
        # El sleep principal del bucle
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")

finally:
    # Siempre limpiar los pines al salir
    print("Limpiando pines GPIO...")
    pwm.stop()
    GPIO.cleanup()