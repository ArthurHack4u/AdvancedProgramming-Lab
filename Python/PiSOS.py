import RPi.GPIO as GPIO
import time

PIN_LED = 17 
TIEMPO_PUNTO = 0.15 # 0.15 segundos para el punto (•)
TIEMPO_RAYA = 0.5   # 0.5 segundos para la raya (-)
TIEMPO_ESPACIO_LETRA = 0.5 # Espacio entre S, O y S

GPIO.setmode(GPIO.BCM) 
GPIO.setup(PIN_LED, GPIO.OUT)

def punto():
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(TIEMPO_PUNTO)
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(TIEMPO_PUNTO)

def raya():

    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(TIEMPO_RAYA)
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(TIEMPO_PUNTO)

print("Iniciando señal SOS... Presiona CTRL+C para salir.")

try:
    while True:
        # S (• • •)
        punto()
        punto()
        punto()

        time.sleep(TIEMPO_ESPACIO_LETRA)

        # O (- - -)
        raya()
        raya()
        raya()

        time.sleep(TIEMPO_ESPACIO_LETRA)

        # S (• • •)
        punto()
        punto()
        punto()

        time.sleep(1.5)

except KeyboardInterrupt:
    print("\nPrograma SOS detenido.")

finally:
    GPIO.cleanup()