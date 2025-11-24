# Práctica 6: Implementación del Protocolo HTTP en Raspberry Pi Zero

**Moran Escalante Bryan Arturo**

**Inurreta del Valle Rafael Enrique**

**Gonzalez Maas Kerin del Jesus**

**Gonzalez Maas Kevin del Jesus** 

---

## 📋 Descripción
Este proyecto consiste en la implementación manual de un servidor HTTP utilizando Sockets en Python (sin frameworks como Flask o Django). El objetivo es gestionar recursos (sensores) a través de una API RESTful cumpliendo con los estándares del protocolo HTTP.

El sistema es capaz de procesar peticiones crudas, parsear cabeceras y cuerpos JSON, y gestionar los métodos **POST** y **DELETE**.

## 📂 Estructura del Proyecto

* **`server.py`**: Script principal que inicia el servidor, gestiona las conexiones, enruta las peticiones e implementa la lógica de negocio (validaciones, almacenamiento en memoria).
***`http_parser.py`**: Módulo encargado de desglosar la petición HTTP cruda en Método, URI, Cabeceras y Cuerpo (Body).

## ⚙️ Requisitos
* Python 3.x
* Raspberry Pi Zero (o cualquier entorno Linux/Windows/Mac para pruebas).
* Librerías estándar: `socket`, `json`, `datetime` (no requiere instalación externa).

## 🚀 Instalación y Ejecución

1.  Clona o descarga los archivos en tu dispositivo.
2.  Abre una terminal en la carpeta del proyecto.
3.  Ejecuta el servidor:

```bash
python3 server.py
```
El servidor iniciará escuchando en 0.0.0.0:8080

## 📡 Documentación de la API

### 1. Crear un Sensor (POST)
Crea un nuevo recurso en el sistema. Valida tipos de datos y unicidad del ID.

* **Endpoint:** `/api/sensors`
* **Método:** `POST`
* **Headers:** `Content-Type: application/json`

**Cuerpo (JSON):**
* `sensor_id` (string, obligatorio, único)
* `name` (string, obligatorio)
* `value` (number, obligatorio)
* `unit` (opcional)
* `location` (opcional)

**Respuesta Exitosa:**
* **Código:** `201 Created`
* **Body:** Objeto JSON con el sensor creado y timestamps (`created_at`, `updated_at`).

---

### 2. Eliminar un Sensor (DELETE)
Elimina un recurso existente basado en su ID.

* **Endpoint:** `/api/sensors/{id}`
* **Método:** `DELETE`

**Respuesta Exitosa:**
* **Código:** `200 OK`
* **Body:** Confirmación con ID eliminado y timestamp de la operación.

**Errores Comunes:**
* `400 Bad Request`: JSON malformado o faltan campos obligatorios.
* `404 Not Found`: El sensor a eliminar no existe.

---

## 🧪 Pruebas (Ejemplos con cURL)
Puedes probar la API desde otra terminal mientras `server.py` está corriendo:

**Prueba 1: Crear un Sensor (Correcto)**
```bash
curl -X POST http://localhost:8080/api/sensors \
     -H "Content-Type: application/json" \
     -d '{"sensor_id": "S01", "name": "Temp Lab", "value": 24.5, "unit": "C"}'
```
**Prueba 2: Intentar duplicar ID (Error esperado)**
```bash
curl -X POST http://localhost:8080/api/sensors \
     -H "Content-Type: application/json" \
     -d '{"sensor_id": "S01", "name": "Copia", "value": 30}'
```
**Prueba 3: Eliminar Sensor**
```bash
curl -X DELETE http://localhost:8080/api/sensors/S01
```