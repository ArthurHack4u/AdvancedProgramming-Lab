import RPi.GPIO as GPIO
import time

PIN_LED = 17 
PIN_BOTON = 2 

TIEMPO_PUNTO = 0.15 
TIEMPO_RAYA = 0.5   
TIEMPO_ESPACIO_LETRA = 0.5 
TIEMPO_REPOSO = 5 

GPIO.setmode(GPIO.BCM) 

GPIO.setup(PIN_LED, GPIO.OUT) 
GPIO.setup(PIN_BOTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

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

def enviar_sos():
    print("—> ¡SOS detectado! Enviando señal...")
    # S (• • •)
    for _ in range(3):
        punto()

    time.sleep(TIEMPO_ESPACIO_LETRA)

    # O (- - -)
    for _ in range(3):
        raya()

    time.sleep(TIEMPO_ESPACIO_LETRA)

    # S (• • •)
    for _ in range(3):
        punto()

    print("—> Señal SOS completada. Esperando pausa...")
    time.sleep(TIEMPO_REPOSO)


print("Esperando que se presione el botón (GPIO 2)... Presiona CTRL+C para salir.")

try:
    while True:
        GPIO.wait_for_edge(PIN_BOTON, GPIO.FALLING)

        enviar_sos()

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")

finally:
    GPIO.cleanup()