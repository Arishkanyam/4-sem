import socket
from threading import Thread

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Ошибка при получении сообщения от сервера.")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        try:
            message = input()
            client_socket.send(message.encode())
            if message.lower() == 'exit':
                client_socket.close()
                break
        except:
            print("Ошибка при отправке сообщения.")
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5050))

    username = input("Введите ваше имя: ")
    client_socket.send(username.encode())

    print(client_socket.recv(1024).decode())
    print("Ожидаем приветствие от сервера...")

    receive_thread = Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == '__main__':
    start_client()