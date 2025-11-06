import RPi.GPIO as GPIO
import time

class Potentiometer:
    """
    Clase para encapsular la lógica de lectura y calibración
    de un potenciómetro en la Raspberry Pi usando el método de
    carga de capacitor.
    """
    def __init__(self, pin):
        """
        Inicializa el potenciómetro.
        :param pin: El número de pin BCM al que está conectado el potenciómetro.
        """
        self.pin = pin
        self.min_value = 0
        self.max_value = 1000  # Un valor por defecto
        # Asumimos que GPIO.setmode(GPIO.BCM) se llama fuera de la clase

    def read_raw_value(self):
        """
        Lee el valor crudo del potenciómetro midiendo el tiempo de carga.
        :return: Un entero que representa el valor crudo (tiempo de carga).
        """
        count = 0
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.01)
        
        GPIO.setup(self.pin, GPIO.IN)
        while GPIO.input(self.pin) == GPIO.LOW:
            count += 1
            if count > 100000:  # Timeout de seguridad
                break
        return count

    def calibrate(self):
        """
        Guía al usuario para calibrar los valores mínimo y máximo
        del potenciómetro.
        :return: Tupla (min_value, max_value)
        """
        print("--- Iniciando Calibración del Potenciómetro ---")
        input("Gira el potenciómetro completamente a la izquierda (0 grados) y presiona Enter.")
        self.min_value = self.read_raw_value()
        print(f"Valor mínimo registrado: {self.min_value}")
        
        print("-" * 20)
        
        input("Ahora, gira el potenciómetro completamente a la derecha (180 grados) y presiona Enter.")
        # Leer varias veces para obtener un máximo estable
        max_vals = [self.read_raw_value() for _ in range(3)]
        self.max_value = max(max_vals)
        print(f"Valor máximo registrado: {self.max_value}")
        
        print("-" * 20)
        
        if self.max_value <= self.min_value:
            print("Advertencia: El valor máximo y mínimo son iguales. Asignando rango por defecto.")
            self.max_value = self.min_value + 1000
        
        print("¡Calibración completada!")
        return self.min_value, self.max_value

    def get_normalized_value(self):
        """
        Devuelve el valor del potenciómetro normalizado entre 0.0 y 1.0,
        basado en la calibración.
        :return: Float entre 0.0 y 1.0.
        """
        raw_value = self.read_raw_value()
        normalized = (raw_value - self.min_value) / (self.max_value - self.min_value)
        # Aplicar "clamping" para asegurar que el valor esté entre 0 y 1
        normalized = max(0.0, min(1.0, normalized))
        return normalized
