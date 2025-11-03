# 💬 Chat Concurrente en Java

Este es un proyecto de un chat simple basado en Sockets de Java. Implementa un servidor concurrente capaz de manejar múltiples clientes de forma simultánea, permitiendo la comunicación global, mensajes privados y cambio de nombre de usuario.

## 🚀 Características

* **Servidor Concurrente:** Utiliza hilos (`Thread`) para manejar a cada cliente de forma independiente, permitiendo múltiples conexiones simultáneas.
* **Lista Segura de Clientes:** Usa `CopyOnWriteArrayList` para prevenir problemas de concurrencia al añadir o eliminar clientes.
* **Chat Global:** Los mensajes enviados por defecto se transmiten a todos los demás usuarios conectados.
* **Mensajes Privados:** Envía mensajes a un usuario específico usando el comando `/pm`.
* **Cambio de Nombre:** Los usuarios pueden cambiar su nombre en cualquier momento con el comando `/nick`.
* **Notificaciones:** El chat informa cuándo un usuario se une, se va o cambia de nombre.
* **Cliente Flexible:** El cliente solicita la IP y el puerto al iniciarse, permitiendo conectarse a cualquier servidor.

## 🛠️ Tecnologías Utilizadas

* **Java**
* **Sockets de Java** (`java.net.Socket` y `java.net.ServerSocket`)
* **Hilos de Java** (`Thread` y `Runnable`)
* **Streams de Datos** (`DataInputStream` y `DataOutputStream`)
* **Colecciones Concurrentes** (`CopyOnWriteArrayList`)

## 🔌 Instalación y Ejecución

### Prerrequisitos

* Tener instalado el **JDK de Java** (versión 8 o superior).

## 📜 Modo de Uso y Comandos

#### El programa te pedirá los datos de conexión:

Introduce la IP del servidor:

Si estás ejecutando el cliente en la misma máquina que el servidor, puedes escribir localhost o 127.0.0.1.

Si está en otra máquina en tu red, escribe la IP de esa máquina.

Introduce el Puerto del servidor:

Escribe 8080 (o el puerto que hayas configurado en Servidor.java).

¡Repite este paso en más terminales para simular múltiples usuarios!
Una vez conectado, todo lo que escribas será un mensaje global por defecto.

## Comandos Disponibles

Cambiar nombre de usuario:

/nick ` <nuevo_nombre>` 

Ejemplo: /nick Juan

Enviar mensaje privado:

/pm `<nombre_de_usuario>`  `<mensaje>`

Ejemplo: /pm Juan Hola, ¿cómo estás?