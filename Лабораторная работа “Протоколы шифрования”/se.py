import socket
import random
from encryption import generate_secret_key, encrypt, decrypt


def generate_keys():
    p = 23
    g = 5
    a = random.randint(1, p - 1)
    A = pow(g, a, p)
    return p, g, a, A


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5050))
    server_socket.listen(1)

    print("Сервер запущен и ожидает подключения клиента...")

    client_socket, client_address = server_socket.accept()
    print("Подключился клиент:", client_address)

    p, g, a, A = generate_keys()

    # Отправка открытого ключа клиента
    client_socket.sendall(str(A).encode())

    # Получение открытого ключа клиента
    B = int(client_socket.recv(1024).decode())

    # Вычисление общего секрета
    secret_key = generate_secret_key(p, a, B)

    print("Общий секрет вычислен.")

    while True:
        # Прием зашифрованного сообщения от клиента
        encrypted_message = client_socket.recv(1024).decode()

        # Дешифрование сообщения с использованием XOR
        decrypted_message = decrypt(encrypted_message, secret_key)

        print("Клиент:", decrypted_message)

        # Ответ клиенту
        response = input("Введите ответ: ")

        # Шифрование ответа с использованием XOR
        encrypted_response = encrypt(response, secret_key)

        # Отправка зашифрованного ответа клиенту
        client_socket.sendall(str(encrypted_response).encode())

        # Проверка условия выхода
        if response.lower() == 'exit':
            break

    # Закрытие соединения
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    run_server()