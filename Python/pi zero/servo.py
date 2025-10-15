import RPi.GPIO as GPIO
import time

SERVO_PIN = 18 
FREQUENCY = 50 

def set_servo_angle(angle):
    pulse_ms = 1.5 - (angle / 90) * 0.5
    duty_cycle = (pulse_ms / 20.0) * 100
    pwm.ChangeDutyCycle(duty_cycle)

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
    pwm.start(0)

    while True:
        print("Moviendo a -90 grados (izquierda)")
        set_servo_angle(-90)
        time.sleep(3)

        print("Moviendo a 0 grados (centro)")
        set_servo_angle(0)
        time.sleep(3)

        print("Moviendo a 90 grados (derecha)")
        set_servo_angle(90)
        time.sleep(3)

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    pwm.stop()
    GPIO.cleanup()
