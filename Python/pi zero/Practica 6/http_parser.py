def parse_http_request(raw_request):
    """
    Desglosa una petición HTTP cruda en sus componentes principales:
    Method, URI, Version, Headers y Body.
    Basado en la estructura descrita en el PDF.
    """
    # Separar la cabecera del cuerpo usando la secuencia \r\n\r\n
    parts = raw_request.split('\r\n\r\n', 1)
    
    header_section = parts[0]
    # Si existe una segunda parte, es el cuerpo (Body); si no, está vacío.
    body = parts[1] if len(parts) > 1 else ""

    lines = header_section.split('\r\n')
    
    # Validación básica de la línea de solicitud
    if not lines or lines[0] == '':
        return None

    # Extraer Method, URI y Version (Ej: POST /api/sensors HTTP/1.1) [cite: 16]
    request_line = lines[0]
    try:
        method, path, version = request_line.split(' ')
    except ValueError:
        return None

    headers = {}
    # Procesar headers a partir de la segunda línea
    for line in lines[1:]:
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

    return {
        'method': method,
        'path': path,
        'version': version,
        'headers': headers,
        'body': body  # Crucial para el método POST [cite: 12]
    }

def create_http_response(status_code, body_content, content_type='application/json'):
    """
    Genera una respuesta HTTP con formato correcto.
    """
    status_map = {
        200: 'OK',
        201: 'Created',       # Requerido para POST exitoso [cite: 59]
        400: 'Bad Request',   # Requerido para errores de validación [cite: 61]
        404: 'Not Found',     # Requerido para DELETE si no existe [cite: 71]
        500: 'Internal Server Error'
    }

    reason = status_map.get(status_code, 'Unknown')
    
    # Construcción de la respuesta siguiendo el estándar
    response = f"HTTP/1.1 {status_code} {reason}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(body_content)}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += body_content

    return response