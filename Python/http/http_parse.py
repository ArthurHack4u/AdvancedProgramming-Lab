def parse_http_request(request):
    lines = request.split('\r\n')

    request_line = lines[0]
    method, path, version = request_line.split(' ')

    headers = {}
    idx = 1

    while idx < len(lines) and lines[idx] != '':
        line = lines[idx]

        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

        elif '{' in line and '}' in line:
            key, value = line.split(' ', 1)
            headers[key.strip()] = value.strip()

        idx += 1

    return {
        'method': method,
        'path': path,
        'version': version,
        'headers': headers
    }


def send_http_response(status_code, content, content_type='text/plain', extra_headers=None):
    status_messages = {
        200: 'OK',
        401: 'Unauthorized',
        404: 'Not Found',
        500: 'Internal Server Error'
    }

    response = f"HTTP/1.1 {status_code} {status_messages.get(status_code)}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(content)}\r\n"

    if extra_headers:
        for k, v in extra_headers.items():
            response += f"{k}: {v}\r\n"

    response += "\r\n"
    response += content

    return response
