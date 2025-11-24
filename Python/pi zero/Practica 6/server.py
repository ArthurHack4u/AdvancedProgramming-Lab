import socket
import json
from datetime import datetime
from http_parser import parse_http_request, create_http_response

# Configuración del servidor
HOST = '0.0.0.0'  # Escuchar en todas las interfaces
PORT = 8080

# Base de datos en memoria para almacenar los sensores [cite: 41]
# Estructura: { "sensor_id": { ...datos... } }
sensores_db = {}

def handle_post_request(body):
    """
    Implementa la lógica del Método POST[cite: 42]:
    1. Validar JSON y campos obligatorios.
    2. Validar tipos de datos.
    3. Verificar unicidad.
    4. Guardar con timestamps.
    """
    try:
        if not body:
            return 400, {"error": "Cuerpo de petición vacío"}

        # 1. Extraer y validar formato JSON [cite: 44, 45]
        data = json.loads(body)

        # 2. Verificar presencia de campos obligatorios [cite: 46, 47, 78]
        required_fields = ["sensor_id", "name", "value"]
        for field in required_fields:
            if field not in data:
                return 400, {"error": f"Campo obligatorio faltante: {field}"}

        # 3. Validar tipos de datos [cite: 48, 49, 50, 79]
        if not isinstance(data["sensor_id"], str):
            return 400, {"error": "sensor_id debe ser un string"}
        if not isinstance(data["name"], str):
            return 400, {"error": "name debe ser un string"}
        if not isinstance(data["value"], (int, float)):
            return 400, {"error": "value debe ser numérico"}

        # 4. Comprobar que el sensor_id no exista previamente [cite: 53, 83]
        s_id = data["sensor_id"]
        if s_id in sensores_db:
            return 400, {"error": f"El sensor_id '{s_id}' ya existe"}

        # 5. Generar marcas de tiempo 
        timestamp = datetime.now().isoformat()

        # Crear el objeto recurso completo
        new_sensor = {
            "sensor_id": s_id,
            "name": data["name"],
            "value": data["value"],
            "unit": data.get("unit", "N/A"), # Opcional según validación estricta, pero parte de estructura [cite: 41]
            "location": data.get("location", "N/A"),
            "created_at": timestamp,
            "updated_at": timestamp
        }

        # Almacenar en la estructura de datos [cite: 57, 58]
        sensores_db[s_id] = new_sensor

        # Devolver 201 Created y el recurso creado [cite: 59, 62]
        return 201, {
            "mensaje": "Recurso creado exitosamente",
            "sensor": new_sensor
        }

    except json.JSONDecodeError:
        # Error 400 por JSON malformado [cite: 61]
        return 400, {"error": "JSON malformado"}
    except Exception as e:
        return 500, {"error": str(e)}

def handle_delete_request(path):
    """
    Implementa la lógica del Método DELETE[cite: 63]:
    1. Extraer ID de la URL.
    2. Buscar recurso.
    3. Eliminar o devolver error.
    """
    # La ruta esperada es /api/sensors/{id}
    # Dividimos el path. Ej: ['', 'api', 'sensors', '01']
    parts = path.split('/')
    
    # Validar formato del identificador en la ruta [cite: 66, 87]
    if len(parts) < 4 or parts[3] == "":
        return 400, {"error": "Identificador no proporcionado en la URL"}
    
    sensor_id = parts[3]

    # Lógica de Negocio: Buscar y eliminar [cite: 68, 69, 70]
    if sensor_id in sensores_db:
        # Eliminar recurso
        del sensores_db[sensor_id]
        
        # Estructura de respuesta exitosa [cite: 73, 74, 75]
        response_data = {
            "mensaje": "Recurso eliminado exitosamente",
            "id_eliminado": sensor_id,
            "timestamp": datetime.now().isoformat()
        }
        return 200, response_data # [cite: 71]
    else:
        # 404 Not Found si no existe [cite: 71]
        return 404, {"error": "El recurso especificado no existe"}

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[*] Servidor HTTP iniciado en {HOST}:{PORT}")
    print("[*] Endpoint base: /api/sensors")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            # Recibir datos (buffer de 4096 para permitir JSONs medianos)
            raw_request = client_socket.recv(4096).decode('utf-8')
            
            if not raw_request:
                client_socket.close()
                continue

            # Parsear la petición
            request_data = parse_http_request(raw_request)
            
            if request_data:
                method = request_data['method']
                path = request_data['path']
                body = request_data['body']
                
                print(f"[Petición] {method} {path}")

                response_code = 404
                response_body = {"error": "Ruta no encontrada"}

                # Enrutamiento según especificaciones 
                if path.startswith("/api/sensors"):
                    
                    if method == 'POST' and path == '/api/sensors':
                        response_code, response_body = handle_post_request(body)
                    
                    elif method == 'DELETE':
                        response_code, response_body = handle_delete_request(path)
                    
                    elif method == 'GET':
                         # Extra (no obligatorio pero útil para ver datos)
                         response_code, response_body = 200, list(sensores_db.values())
                    
                    else:
                        response_code = 405 # Method Not Allowed (Opcional)

                # Generar respuesta HTTP cruda
                http_response = create_http_response(
                    response_code, 
                    json.dumps(response_body)
                )
                
                client_socket.sendall(http_response.encode('utf-8'))
            
            client_socket.close()

    except KeyboardInterrupt:
        print("\n[!] Deteniendo servidor...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_server()