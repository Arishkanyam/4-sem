from socket import socket


sock = socket()
host, port = input('Enter "host:port"\n').split(':')  # localhost:5050

try:
    sock.connect((host, int(port)))
except ConnectionError:
    print("Connection error")
else:
    print(f"Connection with {host}:{port} established")
    print('hello world!')
     
    while True:
        try:
            message=(input('Enter message to send: ').encode())
            if not message:
                print('your connection is ended')
                break
            sock.send(message)
        except ConnectionError:
            print('Sending message error')
        else:
            print(f'Message sent to {host}:{port}')

            #answer_blocks = []
            answer_blocks=sock.recv(1024).decode() #append.,
            sock.close ##

            answer = ''.join(answer_blocks)
            print(f'{answer} gotten back from server')

            
sock.close()
