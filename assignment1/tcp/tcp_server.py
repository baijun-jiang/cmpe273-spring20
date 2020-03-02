import socket, threading


TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
client_mapping = []

def handle_client(client_address, client_socket, client_mapping):

    while True:
        data = client_socket.recv(BUFFER_SIZE)

        if not data:
            return

        decoded_data = data.decode()

        if client_address not in client_mapping:
            print(f'Connected Client:{decoded_data.split(":")[0]}')
            client_mapping.append(client_address)

        print(f"received data:{decoded_data}")
        client_socket.send("pong".encode())


def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print(f'Server started at port {TCP_PORT}')

    while True:
        client_socket, client_address = s.accept()
        thread = threading.Thread(target=handle_client, args=(client_address, client_socket, client_mapping))
        thread.start()


listen_forever()