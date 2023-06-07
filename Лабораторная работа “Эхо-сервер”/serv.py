import socket
import struct

def log_message(message):
    """
    Logs message to a file.

    :param message: Message to be logged.
    :type message: str
    """
    with open('log.txt', 'a') as file:
        file.write(message + '\n')

def load_clients():
    """
    Loads clients from file.

    :return: Dictionary of clients.
    :rtype: dict
    """
    try:
        with open('clients.txt', 'r') as file:
            clients = dict(line.strip().split(':') for line in file.readlines())
    except FileNotFoundError:
        clients = {}
    return clients

def save_client(ip, username):
    """
    Saves client to file.

    :param ip: IP address of client.
    :type ip: str
    :param name: Name of client.
    :type name: str
    """
    print(f'saving client: {ip}:{username}')
    with open('clients.txt', 'a') as file:
        file.write(f'{ip}:{username}\n')

def greet_client(conn, ip, clients):
    """
    Greets client by name if already known, otherwise saves client name.

    :param conn: Connection object.
    :type conn: socket object
    :param ip: IP address of client.
    :type ip: str
    :param clients: Dictionary of clients.
    :type clients: dict
    """
    if ip in clients:
        name = clients[ip]
        send_message_with_header(conn, f'Welcome back, {name}!')
        log_message(f'Welcome back, {name}!') #logger.info
    else:
        name = receive_message_with_header(conn)
        save_client(ip, name)
        send_message_with_header(conn, f'Welcome, {name}!')
        log_message(f'Welcome, {name}!')     #logger.info

def send_message_with_header(conn, message):
    """
    Sends message with header length.

    :param conn: Connection object.
    :type conn: socket object
    :param message: Message to be sent.
    :type message: str
    """
    message_length = len(message)
    header = struct.pack('!I', message_length)
    conn.sendall(header + message.encode())

def receive_message_with_header(conn):
    """
    Receives message with header length.

    :param conn: Connection object.
    :type conn: socket object
    :return: Received message.
    :rtype: str
    """
    header = conn.recv(4)
    message_length = struct.unpack('!I', header)[0]
    message = conn.recv(message_length)
    return message.decode()

def start_server():
    """
    Starts server and listens for incoming connections.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = input('Enter the server address (default: localhost): ') or 'localhost'
    port = int(input('Enter the port number (default: 5050): ') or 5050)

    try:
        sock.bind((host, port))
        sock.listen(1)
        log_message(f'Server started. Listening on {host}:{port}')  #logger.info
        print(f'Server started. Listening on {host}:{port}')

        while True:
            conn, addr = sock.accept()
            ip = addr[0]
            clients = load_clients()

            greet_client(conn, ip, clients)

            while True:
                message = receive_message_with_header(conn)
                if not message:
                    log_message(f'Client {ip} has disconnected')    #logger.info
                    print(f'Client {ip} has disconnected')
                    break

                log_message(f'Received message from {ip}: {message}')      #logger.info
                print(f'Received message from {ip}: {message}')
                send_message_with_header(conn, f'Echo: {message}')

    except socket.error as e:
        log_message(f'Socket error: {str(e)}') #logger.error

    finally:
        sock.close()
        log_message('Server closed')   #logger.info

start_server()