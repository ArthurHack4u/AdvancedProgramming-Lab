# 📝 README – Servidor HTTP en Python

## 📌 Descripción
Servidor HTTP simple implementado con **sockets**, capaz de:
- Procesar rutas (`/`, `/api/hora`, `/admin`)
- Leer y parsear peticiones HTTP crudas
- Manejar autenticación mediante headers

---

## 📂 Archivos del proyecto
```
server.py        → Servidor HTTP
http_parse.py    → Parser y generador de respuestas
send_request.py  → Cliente para pruebas
```

---

## 🚀 Rutas soportadas
| Ruta        | Respuesta |
|-------------|-----------|
| `/`         | Hola mundo |
| `/api/hora` | Hora actual del sistema |
| `/admin`    | Requiere autenticación |

---

## 🔐 Autenticación

El servidor acepta **tres formatos diferentes**:

```
token: 1234
Authorization:{token:1234}
Authorization {token:1234}
```

Token válido:
```
1234
```

Respuestas:
- ✔️ 200 OK → Admin autenticado  
- ❌ 401 Unauthorized → Token inválido

---

## 📡 Conexión desde otros equipos

El servidor usa:
```
host = "0.0.0.0"
port = 8080
```

Permite que el profesor se conecte desde su computadora usando:

```
http://TU-IP:8080
```

Para obtener tu IP(en MacOS):
```
ipconfig getifaddr en0
```

---

## 🧪 Ejemplo de request del profesor

```http
GET /admin/ HTTP/1.1
Host: localhost
Authorization:{token:1234}
```

---

## ▶️ Ejecución

### **Servidor**
```
python3 server.py
```

### **Cliente de prueba**
```
python3 send_request.py
```

---
