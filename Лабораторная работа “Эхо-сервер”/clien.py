import socket
import struct
import hashlib

def log_message(message):
    """
    Logs a message to a log file.

    :param message: Message to be logged.
    :type message: str
    """
    with open('log.txt', 'a') as file:
        file.write(message + '\n')

def load_users():
    """
    Loads users and their hashed passwords from a file.

    :return: Dictionary containing users and their hashed passwords.
    :rtype: dict
    """
    try:
        with open('users.txt', 'r') as file:
            users = dict(line.strip().split(':') for line in file.readlines())
    except FileNotFoundError:
        users = {}
    return users

def hash_password(password):
    """
    Hashes a password using SHA-256 algorithm.

    :param password: Password to be hashed.
    :type password: str
    :return: Hashed password.
    :rtype: str
    """
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(username, password):
    """
    Saves a user and their hashed password to a file.

    :param username: Username of the user to be saved.
    :type username: str
    :param password: Password of the user to be saved.
    :type password: str
    """
    with open('users.txt', 'a') as file:
        file.write(f'{username}:{hash_password(password)}\n')

def authenticate(conn):
    """
    Authenticates a user by checking their username and password.

    :param conn: Connection object.
    :type conn: socket.socket
    """
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    
    users = load_users()
    if username in users:
        if hash_password(password) == users[username]:
            conn.send(b'Success')
            log_message("User authenticated successfully.")  #logger.info
            print("User authenticated successfully.")
        else:
            conn.send(b'Invalid credentials')
            log_message("Invalid credentials entered.")    #logger.warning
            print("Invalid credentials entered.")
    else:
        save_user(username, password)
        conn.send(b'User registered')
        log_message("New user registered.")   #logger.info
        print("New user registered.")

def send_message_with_header(conn, message):
    """
    Sends a message with a header containing the length of the message.

    :param conn: Connection object.
    :type conn: socket.socket
    :param message: Message to be sent.
    :type message: bytes
    """
    message_length = len(message)
    header = struct.pack('!I', message_length)
    conn.sendall(header + message)

def receive_message_with_header(conn):
    """
    Receives a message with a header containing the length of the message.

    :param conn: Connection object.
    :type conn: socket.socket
    :return: Received message.
    :rtype: str
    """
    header = conn.recv(4)
    if not header:
        return ''
    message_length = struct.unpack('!I', header)[0]
    message = conn.recv(message_length)
    return message.decode()

def start_client():
    """
    Starts the client and connects to the server.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = input('Enter the server address (default: localhost): ') or 'localhost'
    port = int(input('Enter the port number (default: 5050): ') or 5050)

    try:
        sock.connect((host, port))
        log_message(f'Connected to the server at {host}:{port}')   #logger.info
        print(f'Connected to the server at {host}:{port}')
        authenticate(sock)

        while True:
            message = input('Enter a message to send (press Enter to exit): ').encode()
            send_message_with_header(sock, message)
            if not message:
                log_message('Your connection is ended')   #logger.info
                print('Your connection is ended')
                break

            try:
                answer = receive_message_with_header(sock)
                log_message(f'Received data from the server: "{answer}"')   #logger.info
                print(f'Received data from the server: "{answer}"') 

            except socket.error as e:
                log_message(f'Socket error: {str(e)}')  #logger.error

    except socket.error as e:
        log_message(f'Connection error: {str(e)}')    #logger.error

    finally:
        sock.close()
        log_message('Disconnected from the server')    #logger.info
        print('Disconnected from the server')


start_client()