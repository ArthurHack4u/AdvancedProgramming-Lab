import socket

def send_request(raw_request):
    s = socket.socket()
    s.connect(("localhost", 8080))
    s.send(raw_request.encode())
    response = s.recv(4096).decode()
    s.close()
    print(response)


req1 = (
    "GET / HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "\r\n"
)

req2 = (
    "GET /api/hora HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "\r\n"
)

req3 = (
    "GET /admin HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "token: 1234\r\n"
    "\r\n"
)

req4 = (
    "GET /admin HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "authorization {token:1234}\r\n"
    "\r\n"
)

send_request(req1)
send_request(req2)
send_request(req3)
send_request(req4)
