from itertools import islice
import socket, pickle, time, getopt, sys, datetime


UDP_IP = '127.0.0.1'
UDP_PORT = 4000
BUFFER_SIZE = 4096
MESSAGE = "ping"
RETRY = 5
TIMEOUT = 1
BACKOFF = 3

def stream_input_as_batch(id):
    with open('./upload.txt', 'r') as file:
        batch_no = 0
        while True:
            batch = list(islice(file, 100))

            if not batch:
                yield (None, None, None, id, True)
                break

            yield (batch, len(batch), batch_no, id, False)
            batch_no = batch_no + 1

def upload_by_batch(socket, batch):
    try:
        socket.sendto(pickle.dumps(batch), (UDP_IP, UDP_PORT))
        data, ip = socket.recvfrom(BUFFER_SIZE)
        decoded_data = pickle.loads(data)
        sig = int(decoded_data.get("ack"))

        if len(data) is not None and (sig == sys.maxsize or sig == batch[2]):

            if sig == sys.maxsize:
                print("File upload successfully completed.")
                return 0

            print(f'recieved acknowledgement {decoded_data.get("ack")} from server')
            return 0

        else: 
            raise AcknowlegemntError("ack error")

    except Exception as e:
        print(f'did not recieve acknowledgement from server')
        retry = 0
        while retry < RETRY:
            try:
                print(f'resending pacakge')
                socket.sendto(pickle.dumps(batch), (UDP_IP, UDP_PORT))
                data, ip = socket.recvfrom(BUFFER_SIZE)

                if len(data) is not None:
                    data = pickle.loads(data)

                    if int(data.get("ack")) == batch[2]:
                        print(f'recieved acknowledgement {data.get("ack")} from server')
                        return 0
                    # wrong package acknowledgement
                    else:
                        retry = retry + 1
                        time.sleep(BACKOFF * retry)
                # not recieving acknowledgement
                else:
                    retry = retry + 1
                    time.sleep(BACKOFF * retry)
            # socket errors
            except:
                retry = retry + 1
                time.sleep(BACKOFF * retry)

        if batch[4]:
            return -2

        return -1



def send(id=0, delay=3):
    time.sleep(int(delay))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(TIMEOUT)
        batch_gen = stream_input_as_batch(id)

        print("Connected to Server")
        print("Starting a file (upload.txt) upload...")

        for batch in batch_gen:
            time.sleep(1)
            sig = upload_by_batch(s, batch)

            if sig == -1:
                print(f"Client {id} have not recieved acknowledgement from server, abort upload")
                return
            if sig == -2:
                print("Client have finished upload and sent terminate signal but didn't recieve acknowledgement from server")
                return 
        return
        
    except socket.error:
        print("Error! {}".format(socket.error))
        exit()


def get_client_info():
    opts, args = getopt.getopt(sys.argv, None)
    args = args[1:]
    if len(args) > 2:
        print("Input Arg Error. Only accept two params: 1. id(str), 2. delay timer(int)")
        exit()
    args[0] = f'{args[0]}_{datetime.datetime.now().timestamp()}'
    return args

send(*get_client_info())

class AcknowlegemntError(Exception):
    pass