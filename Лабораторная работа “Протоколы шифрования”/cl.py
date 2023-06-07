import socket
import random
from encryption import generate_secret_key, encrypt, decrypt


def generate_keys():
    p = 23
    g = 5
    a = random.randint(1, p - 1)
    A = pow(g, a, p)
    return p, g, a, A


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5050))

    print("Подключение к серверу установлено.")

    p, g, a, A = generate_keys()

    # Отправка открытого ключа серверу
    client_socket.sendall(str(A).encode())

    # Получение открытого ключа сервера
    B = int(client_socket.recv(1024).decode())

    # Вычисление общего секрета
    secret_key = generate_secret_key(p, a, B)

    print("Общий секрет вычислен.")

    while True:
        # Отправка сообщения серверу
        message = input("Введите сообщение: ")

        # Шифрование сообщения с использованием XOR
        encrypted_message = encrypt(message, secret_key)

        # Отправка зашифрованного сообщения серверу
        client_socket.sendall(str(encrypted_message).encode())

        # Проверка условия выхода
        if message.lower() == 'exit':
            break

        # Прием зашифрованного ответа от сервера
        encrypted_response = client_socket.recv(1024).decode()

        # Дешифрование ответа с использованием XOR
        response = decrypt(encrypted_response, secret_key)

        print("Сервер:", response)

    # Закрытие соединения
    client_socket.close()


if __name__ == '__main__':
    run_client()
