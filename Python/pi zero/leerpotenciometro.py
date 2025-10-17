import RPi.GPIO as GPIO
import time

POT_PIN = 4
GPIO.setmode(GPIO.BCM)

def read_potentiometer():
    count = 0
    GPIO.setup(POT_PIN, GPIO.OUT)
    GPIO.output(POT_PIN, GPIO.LOW)
    time.sleep(0.01)
    
    GPIO.setup(POT_PIN, GPIO.IN)
    while GPIO.input(POT_PIN) == GPIO.LOW:
        count += 1
        if count > 100000: # Timeout generoso
            return -1
    return count

try:
    print("Leyendo valores del potenciómetro. Gira la perilla. (Ctrl+C para salir)")
    while True:
        value = read_potentiometer()
        print(f"Valor leído: {value}")
        time.sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
