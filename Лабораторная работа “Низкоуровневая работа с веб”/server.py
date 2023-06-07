import socket
from datetime import datetime

file = input('Choose file to open:\n1. 1.html\n2. 2.html\n3. indexx.html\n4. image.png\nFile name: ') #у меня в другом проекте файл index.html, не хочу их спутать

if file=='1.html':
    filename = '1.html'
    content_type = 'text/html'
elif file=='2.html':
    filename = '2.html'
    content_type = 'text/html'
elif file=='indexx.html':
    filename = 'indexx.html'
    content_type = 'text/html'
elif file == 'image.png':
    filename = 'image.png'
    content_type = 'image/png'
else: 
    print('Invaid file choice')
    exit()

    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  
    try:
        sock.bind(('localhost', 80))
        print('Using port 80')
    except OSError:
        sock.bind(('localhost', 8080))
        print('Using port 8080')

    sock.listen(5)

    conn, addr = sock.accept()
    print('Connected', addr)

    data = conn.recv(8192)
    msg = data.decode()

    print(msg)

    with open(filename, 'rb') as f:
        content = f.read()

    if content_type == 'text/html':
        response_body = b"Hello, webworld!"
    else:
        response_body = content

    response_headers = [
        b"HTTP/1.1 200 OK",
        b"Server: SelfMadeServer v0.0.1",
        f"Content-Type: {content_type}".encode(),
        b"Connection: close",
        b"",
    ]

    resp = b"\r\n".join(response_headers) + b"\r\n" + response_body

    conn.send(resp)
    conn.close()

    log_string = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {addr[0]} {filename}"
    with open('server.log', 'a') as log_file:
        log_file.write(log_string + '\n')