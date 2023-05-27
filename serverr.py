from socket import socket


sock = socket()
print('Server started here')

host, port = input('Enter "host:port"\n').split(':')  # localhost:5050

sock.bind((host, int(port)))
sock.listen(1)
print('Port listening started')
conn, addr = sock.accept()
addr = addr[0]
print(f'New connection: {addr}')

while True:
    
    #data_blocks = []
    #while True:
    data_blocks=conn.recv(1024).decode()  # )data_blocks.append(
        #if len(data_blocks[-1]) < 1024:
            #break"""
    data = ''.join(data_blocks)
    if not data:
        print('client is gone')
        conn.close()
        print(f'End of connection with {addr}')
    else: #
        data = ''.join(data_blocks)
        print(f'"{data}" received from {addr}')

        data_back = data.encode()
        conn.send(data_back)
        print(f'{data_back} sent back to client')  
     
sock.close()

print('Stop mainloop')
