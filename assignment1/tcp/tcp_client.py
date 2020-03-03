import socket, sys, time, getopt

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024
MESSAGE = "ping"

def send(id=0, delay=3, message_count=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    request_count = 0
    while request_count < int(message_count):
        print(f"Sending data:{MESSAGE}")
        s.send(f"{id}:{MESSAGE}".encode())
        data = s.recv(BUFFER_SIZE)
        print("Received data:", data.decode())
        request_count = request_count + 1
        time.sleep(int(delay))
    s.close()
    

def get_client_info():
    opts, args = getopt.getopt(sys.argv, None)
    args = args[1:]
    if len(args) > 3:
        print("Input Arg Error. Only accept two params: 1. id(str), 2. delay timer(int), 3. number of messages(int)")
        exit()
    return args


send(*get_client_info())