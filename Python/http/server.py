import socket
import time
from http_parse import parse_http_request, send_http_response

TOKEN_ADMIN = "1234"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = "0.0.0.0"
    port = 8080

    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Servidor iniciado en {host}:{port}")

    def extract_token(headers):

        if "token" in headers:
            return headers["token"].strip()

        if "Authorization" in headers:
            raw = headers["Authorization"]

            raw = raw.replace(" ", "")

            raw = raw.strip("{}")

            if ":" in raw:
                key, value = raw.split(":", 1)
                return value.strip()

        if "authorization" in headers:
            raw = headers["authorization"]
            raw = raw.replace(" ", "")
            raw = raw.strip("{}")

            if ":" in raw:
                key, value = raw.split(":", 1)
                return value.strip()

        return None

    def handler_path(parsed):
        path = parsed["path"]
        headers = parsed["headers"]

        if path == "/" or path == "":
            return send_http_response(200, "Hola mundo desde handler")

        if path == "/api/hora":
            hora = time.strftime("%H:%M:%S")
            return send_http_response(200, f"Hora actual: {hora}")

        if path == "/admin" or path == "/admin/":
            token = extract_token(headers)

            print("Token recibido:", token)

            if token == TOKEN_ADMIN:
                return send_http_response(200, "Admin autenticado")
            else:
                return send_http_response(401, "Token inválido bro")

        return send_http_response(404, "Ruta no encontrada")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"\n📡 Conexión de: {client_address}")

            request_data = client_socket.recv(1024).decode('utf-8')
            parsed = parse_http_request(request_data)

            print("📥 Petición:", parsed)
            print("📍 Ruta:", parsed.get("path"))

            response = handler_path(parsed)
            client_socket.send(response.encode('utf-8'))
            client_socket.close()

    except KeyboardInterrupt:
        print("Apagando servidor...")

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
