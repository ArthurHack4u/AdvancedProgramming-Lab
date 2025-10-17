### Integrantes
Moran Escalante Bryan Arturo

Inurreta del Valle Rafael Enrique

Gonzalez Maas Kerin del Jesus

Gonzalez Maas Kevin del Jesus
# Control de servomotor con Raspberry Pi Zero
Este es un script simple en Python para controlar un servomotor utilizando los pines GPIO de una Raspberry Pi. El programa realiza un barrido continuo, moviendo el servo a las posiciones de -90°, 0° y 90° con pausas de 3 segundos entre cada movimiento.

## Características
- Control Preciso: Utiliza PWM (Modulación por Ancho de Pulso) para posicionar el servomotor en ángulos específicos.

- Movimiento Cíclico: Barre continuamente entre las posiciones izquierda (-90°), centro (0°) y derecha (90°).

# Uso
- Abre una terminal en tu Raspberry Pi.

- Navega hasta el directorio donde guardaste el archivo

Ejecuta el script con el siguiente comando:

- ```python3 servo.py```

Para detener el programa, presiona Ctrl+C. El script detectará la interrupción, detendrá el PWM y limpiará los pines GPIO antes de salir.