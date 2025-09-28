import RPi.GPIO as GPIO
import time

PIN_LED = 17 

GPIO.setmode(GPIO.BCM) 

GPIO.setup(PIN_LED, GPIO.OUT)

print("LED parpadeando. Presiona CTRL+C para salir.")

try:
    while True:
        GPIO.output(PIN_LED, GPIO.HIGH)
        time.sleep(0.5)

        GPIO.output(PIN_LED, GPIO.LOW)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario")

finally:
    GPIO.cleanup()