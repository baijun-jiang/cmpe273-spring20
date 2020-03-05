# Assignment 1 - Part B

You will be adding package lost detection and reliable message delivery to UDP.

## Requirements

* Implement a simple acknowledgement protocol that you assign unique sequence id for each package you send to the server.
* Once the package is received by the server, the server will send acknowledgement back to the client.
* In case of package lost, the client did not receive the acknowledgement back from the server, the client must resend the same package again until you get the acknowledgement.
* To control the package order, the client will never send the next package until it gets the acknowledegement for the previous one.

## Expected Output

* Starting UDP Server

```
python3 udp_server.py

Server started at port 4000.
Accepting a file upload...
Upload successfully completed.
```

* Running UDP Client

```
python3 udp_client.py

Connected to the server.
Starting a file (upload.txt) upload...
Received ack(xxxxxx) from the server.
Received ack(xxxxxx) from the server.
.
..
File upload successfully completed.
```

## acknowledge protocol and server file download explained

* udp client uploads file by batches.
* udp server saves client uploaded file in a folder with {client_id}_{timestamp}_{client_ip}_{client_port}.
Each batch that udp client uploads are saved as a small chunck(file), and a meta file is used to maintain 
or describe udp client uploaded file. After udp client file has completed upload, a upload file will also
being generated within the client upload folder.
* acknowledge protocol: udp client will send a batch to udp server with a batch id, after udp server has processed
the batch, the server will send the processed batch no back to udp client. If udp server/client didn't receive any ack
pacakage, the udp client/server will keep sending the pacakge untill they recieve ack. After exponential back off, the file
upload will be aborted by the client.