import socket, pickle, sys, os

UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 4096

client_dir_mapping = []

def write_to_file(data, batch_no, client_id, client_address):
    dir_path = f'./client_{client_id}_{client_address[0]}_{client_address[1]}'

    if dir_path not in client_dir_mapping and not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        print("Accepting a file upload...")
        client_dir_mapping.append(dir_path)

    file_path= f'{dir_path}/{batch_no}.txt'

    # detect if client didn't receive ack package but server has processed the request pacakge
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        return True

    f = open(file_path, 'a+')
    for line in data:
        if line is None or len(line) == 0:
            return False
        f.write(line)
    return True

def package_verify(package):
    if package[4] == True:
        return (False, True)
    if len(package[0]) != package[1]:
        return (False, False)
    for data in package[0]:
        if len(data) == 0:
            return (False, False)
    return (True, False)

def listen_forever():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((UDP_IP, UDP_PORT))

    while True:
        # get the data sent to us
        data, ip = s.recvfrom(BUFFER_SIZE)
        if len(data) is not None:
            data = pickle.loads(data)
            is_valid = package_verify(data)
            if is_valid[0]:
                client_id = data[3]
                succ = write_to_file(data[0], data[2], data[3], ip)
                if succ:
                    ack = pickle.dumps({"ack": data[2], "completed": False})
                    s.sendto(ack, ip)
            if is_valid[1]:
                print("Upload successfully completed.")
                s.sendto(pickle.dumps({"ack": sys.maxsize, "completed": True}), ip)


listen_forever()