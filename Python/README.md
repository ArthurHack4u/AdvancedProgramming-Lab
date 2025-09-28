# 🚨 Raspberry Pi Zero W - Proyectos GPIO Básicos 🚨

Este repositorio contiene scripts de Python diseñados para ser ejecutados en una **Raspberry Pi Zero W** (o cualquier modelo de Raspberry Pi) para interactuar con los pines **GPIO** (General Purpose Input/Output) y componentes físicos.

Todos los scripts utilizan la librería `RPi.GPIO` y el modo de numeración **BCM**.

## 🔌 Requisitos de Hardware

Para ejecutar los proyectos, necesitarás:

| Componente | Uso | Pin Principal (BCM) |
| :--- | :--- | :--- |
| **Raspberry Pi** | Zero W o cualquier modelo | N/A |
| **LED** | Indicador visual | **GPIO 17** |
| **Resistencia** | 220 ohmios (para proteger el LED) | N/A |
| **Botón Pulsador** | Activar la secuencia | **GPIO 2** |
| **Cables Jumper** | Conexiones | N/A |

### Esquema de Conexión (Resumen)

* **LED:** Patas Larga (Ánodo) $\rightarrow$ Resistencia $\rightarrow$ **GPIO 17**. Pata Corta (Cátodo) $\rightarrow$ **GND**.
* **Botón Pulsador:** Una pata $\rightarrow$ **GPIO 2**. La otra pata $\rightarrow$ **GND**.

---

### Ejecución
```bash
python3 PiParpadeo.py
python3 PiPush.py
python3 PiSOS.py