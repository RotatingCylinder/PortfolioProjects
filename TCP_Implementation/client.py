import sys
import threading
import socket

# Validating port number
port_num = 0
while port_num < 1025 or port_num > 65535:
    port_num = int(input("Please enter valid port number (1025-65535): "))

localhost = "localhost"

# Connecting to server
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((localhost, port_num))
except:
    print("Connection refused, please try with valid port number.")
    sys.exit(0)

# Writing to server
def send_message():
    while True:
        message = input("Client: ")
        client.send(message.encode('utf-8'))

        # Shutdown client when graceful exit occurs
        if message.upper().strip() == "EXIT":
            client.close()
            sys.exit(0)

# Receiving from server
def receive():
    while True:
        # Exception forcefully breaks out of loop when server is shut down
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            break


# Creating and starting threads for receive and send_message functions
# Allow client to send to and receive from server concurrently
client_receive_thread = threading.Thread(target=receive)
client_message_thread = threading.Thread(target=send_message)

client_receive_thread.start()
client_message_thread.start()