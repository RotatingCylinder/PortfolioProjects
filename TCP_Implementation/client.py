import sys
import threading
import socket
from datetime import datetime

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

username = input("Please enter your username: ")

# Writing to server
def send_message():
    # Exception forcefully breaks out of loop when server is shut down
    while True:
        try:
            # Check for client connection
            if client is None:
                break

            # Send message to server
            message_time = datetime.now().strftime("%H:%M")
            message = input()
            client.send(f"[{message_time}]{username}: {message}".encode('utf-8'))
            print(f"[{message_time}]{username}: {message}")

            # Shutdown client when graceful exit occurs
            if message.upper().strip() == "EXIT":
                client.close()
                break
        except:
            break

# Receiving from server
def receive():
    while True:
        # Exception forcefully breaks out of loop when server is shut down
        try:
            # Receive message
            message = client.recv(1024).decode('utf-8')

            # If server is sending "", then server has shutdown
            if not message:
                client.close()
                break

            # Sending client username if server asks for it
            if message == "username":
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            break


# Creating and starting threads for receive and send_message functions
# Allows client to send to and receive from server concurrently
client_receive_thread = threading.Thread(target=receive)
client_message_thread = threading.Thread(target=send_message)

client_receive_thread.start()
client_message_thread.start()