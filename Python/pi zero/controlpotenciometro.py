import RPi.GPIO as GPIO
import time

# Configuración
POT_PIN = 4
SERVO_PIN = 18
FREQUENCY = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
# servo en 0 grados (duty cycle de 2.5)
pwm.start(2.5)

def read_potentiometer():
    """
    Lee el valor del potenciómetro midiendo el tiempo de carga de un capacitor.
    Este método es útil para leer sensores analógicos en pines digitales.
    """
    count = 0
    
    # Descargar el capacitor
    GPIO.setup(POT_PIN, GPIO.OUT)
    GPIO.output(POT_PIN, GPIO.LOW)
    time.sleep(0.01)
    
    # Cambiar el pin a modo de entrada y medir el tiempo hasta que se ponga en alto
    GPIO.setup(POT_PIN, GPIO.IN)
    while GPIO.input(POT_PIN) == GPIO.LOW:
        count += 1
        if count > 50000: # Timeout reducido para 5K
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
    
    if max_val == min_val:
        print("Advertencia: El valor máximo y mínimo son iguales. El servo no se moverá.")
        max_val += 100 

    return min_val, max_val

try:
    min_value, max_value = calibrate()
    
    print("\nControlando el servo con el potenciómetro... (Presiona Ctrl+C para detener)")
    
    while True:
        pot_value = read_potentiometer()
        
        # rango de 0.0 a 1.0
        # Se asegura que el valor no se salga del rango 0-1 con min() y max()
        normalized_value = (pot_value - min_value) / (max_value - min_value)
        normalized_value = max(0.0, min(1.0, normalized_value))
        
        # Convertir el valor normalizado a un ángulo entre 0 y 180
        angle = normalized_value * 180
        
        # Mapeo del ángulo a un ciclo de trabajo (duty cycle) 
        duty_cycle = (angle / 18) + 2.5
        
        pwm.ChangeDutyCycle(duty_cycle)
        
        print(f"Valor Pot: {pot_value:5d} -> Ángulo: {angle:5.1f}° -> Duty Cycle: {duty_cycle:4.1f}%")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")

finally:
    print("Limpiando pines GPIO...")
    pwm.stop()
    GPIO.cleanup()