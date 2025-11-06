import RPi.GPIO as GPIO

class Servo:
    """
    Clase para encapsular la lógica de control de un servomotor
    usando PWM en la Raspberry Pi.
    """
    def __init__(self, pin, frequency=50):
        """
        Inicializa el servo.
        :param pin: El número de pin BCM al que está conectado el servo.
        :param frequency: La frecuencia del PWM (usualmente 50Hz para servos).
        """
        self.pin = pin
        self.frequency = frequency
        # Asumimos que GPIO.setmode(GPIO.BCM) se llama fuera de la clase
        GPIO.setup(self.pin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)  # Iniciar en 0, se moverá al primer set_angle
        self.set_angle(0)  # Posición inicial por defecto

    def _calculate_duty_cycle(self, angle):
        """
        Calcula el ciclo de trabajo (duty cycle) para un ángulo dado.
        2.5% para 0 grados, 12.5% para 180 grados (aprox.)
        (angle / 18) + 2.5  <-- Mapeo común
        """
        return (angle / 18) + 2.5

    def set_angle(self, angle):
        """
        Mueve el servo a un ángulo específico.
        :param angle: El ángulo deseado (entre 0 y 180 grados).
        """
        # Tarea 4: "Implementar un mecanismo de seguridad para límites"
        safe_angle = max(0.0, min(180.0, angle))
        
        duty_cycle = self._calculate_duty_cycle(safe_angle)
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        # Tarea 4: "Agregar logging del movimiento del servo"
        # Usar print por simplicidad, pero logging es mejor
        print(f"[Servo] Moviendo a: {safe_angle:.1f}° (Duty Cycle: {duty_cycle:.1f}%)")

    def stop(self):
        """
        Detiene el PWM del servo.
        """
        print("[Servo] Deteniendo PWM.")
        self.pwm.stop()
