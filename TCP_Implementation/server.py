import socketserver
import threading
import sys
from datetime import datetime

# Validating port number
port_num = 0
while port_num < 1025 or port_num > 65535:
    port_num = int(input("Please enter valid port number (1025-65535): "))

# "localhost" connects to local computer, equivalent to IP address 127.0.0.1
localhost = "localhost"

# Stores address of client
client_list = []

class Server(socketserver.BaseRequestHandler):

    # Overridden from handler
    # handle function tells server how to respond to client
    def handle(self):
        client = self.request
        message_time = datetime.now().strftime("%H:%M")

        # Telling client to send username
        client.sendall(bytes("username", encoding='utf-8'))
        username = client.recv(1024).decode('utf-8')

        print(f"[{message_time}] {username} joined the server.")

        # Sending welcome message
        client_list.append(client)
        client.sendall(bytes(f"Welcome {username} to this TCP chatroom. You can type exit to leave.", encoding='utf-8'))


        # While loop to continually receive messages from client
        while True:
            try:
                # Getting current time
                message_time = datetime.now().strftime("%H:%M")

                # Receive and print next message from client
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break

                print(message)

                # Check for graceful exit
                if message.strip().upper() == "EXIT":
                    break
            except:
                break

        print(f"[{message_time}]{username} has left the chat.")
        #client.sendall(bytes(f"[{message_time}]{username} has left the chat.", encoding='utf-8'))
        client_list.remove(client)
        client.close()


def message_client(server):

    while True:
        message_time = datetime.now().strftime("%H:%M")
        message = input()
        print(f"[{message_time}]Server: {message}")

        if message.upper().strip() == "EXIT":
            print(f"[{message_time}]Server shutting down...")

            for client in client_list:
                try:
                    client.sendall(bytes(f"[{message_time}]Server: {message}",encoding = 'utf-8'))
                    client.close()
                except:
                    pass

            server.shutdown()
            server.server_close()
            break

        for client in client_list:
            try:
                client.sendall(bytes(f"[{message_time}]Server: {message}",encoding = 'utf-8'))
            except:
                break

if __name__ == "__main__":
    time = datetime.now().strftime("%H:%M")
    print(f"[{time}] Server created at port: {port_num}, host: {localhost}")

    server = socketserver.ThreadingTCPServer((localhost, port_num), Server)
    threading.Thread(target=message_client,daemon=True, args = (server,)).start()
    server.serve_forever()


