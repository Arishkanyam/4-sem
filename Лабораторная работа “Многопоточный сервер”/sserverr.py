from threading import Thread
import socket
import time


class ChatServer:
    def __init__(self):
        self.server_socket = None
        self.is_listening = True
        self.is_paused = False
        self.logs = []
        self.clients = []
        self.usernames = []

    def broadcast(self, message, sender_username):

        for client, username in zip(self.clients, self.usernames):
            if username != sender_username:
                client.send(f"{sender_username}: {message}".encode())

    def handle_client(self, client_socket, username):

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message.lower() == 'выход':
                    index = self.clients.index(client_socket)
                    self.clients.remove(client_socket)
                    client_socket.close()
                    username = self.usernames[index]
                    self.usernames.remove(username)
                    self.broadcast(f"{username} покинул чат.", username)
                    break
                else:
                    self.broadcast(message, username)
            except:
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close()
                username = self.usernames[index]
                self.usernames.remove(username)
                self.broadcast(f"{username} покинул чат.", username)
                break

    def listen_clients(self):

        while self.is_listening:
            if self.is_paused:
                time.sleep(1)
                continue
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Клиент подключен: {client_address[0]}:{client_address[1]}")
                #client_socket.send("username".encode())
                username = client_socket.recv(1024).decode()
                self.usernames.append(username)
                self.clients.append(client_socket)
                print(f"Имя пользователя: {username}")
                self.broadcast(f"{username} присоединился к чату.", username)
                client_socket.send("Подключение установлено! Добро пожаловать в чат!".encode())
                client_socket.send("Напишите 'exit' для выхода из чата.".encode())
                client_thread = Thread(target=self.handle_client, args=(client_socket, username))
                client_thread.start()
            except socket.error as e:
                print("Ошибка подключения клиента: %s", str(e))

    def handle_control(self):

        while True:
            command = input("Введите команду (pause, resume, stop, show logs, clear logs, clear auth file): ")
            if command == "pause":
                self.is_paused = True
                print("Сервер остановлен.")
            elif command == "resume":
                self.is_paused = False
                print("Сервер возобновлен.")
            elif command == "stop":
                self.is_listening = False
                self.server_socket.close()
                print("Сервер остановлен.")
                for client_socket in self.clients:
                    client_socket.send("выход".encode())
                    client_socket.close()
                break
            elif command == "show logs":
                print("Логи:")
                for log in self.logs:
                    print(log)
            elif command == "clear logs":
                self.logs.clear()
                print("Логи очищены")
            elif command == "clear auth file":
                with open("auth.txt", "w") as file:
                    file.write("")
                print("Файл аутентификации очищен")
            else:
                print("Команда не опознана. Попробуйте еще раз.")

    def start_server(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 5050))
        self.server_socket.listen(5)
        print("Сервер запущен и ждет подключений...")

        control_thread = Thread(target=self.handle_control)
        control_thread.start()

        self.listen_clients()

chat_server = ChatServer()
chat_server.start_server()