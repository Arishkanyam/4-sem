def generate_secret_key(p, a, B):
    secret_key = pow(B, a, p)
    return secret_key

def encrypt(message, key):
    # Шифрование сообщения с использованием XOR
    encrypted_message = []
    for char in message:
        encrypted_char = chr(ord(char) ^ key)  #если сделать str вместо chr, то будет видна работающая кодировка со смайликами
        encrypted_message.append(encrypted_char)
    return ''.join(encrypted_message)


def decrypt(encrypted_message, key):
    # Дешифрование сообщения с использованием XOR
    decrypted_message = []
    for char in encrypted_message:
        decrypted_char = chr(ord(char) ^ key)  #если сделать int вместо ord, то будет видна работающая кодировка со смайликами
        decrypted_message.append(decrypted_char)
    return ''.join(decrypted_message)