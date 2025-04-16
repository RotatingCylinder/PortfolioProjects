import socketserver
import threading
from datetime import datetime

# Validating port number
port_num = 0
while port_num < 1025 or port_num > 65535:
    try:
        port_num = int(input("Please enter valid port number (1025-65535): "))
    except ValueError:
        print("Please enter an integer")

# "localhost" connects to local computer
localhost = "localhost"

# To reference clients
client_list = []

class TCPServer(socketserver.BaseRequestHandler):

    # Overridden from BaseRequestHandler
    # handle function tells server how to respond to client
    def handle(self):
        client = self.request
        message_time = datetime.now().strftime("%H:%M")

        # Telling client to send username
        client.send(bytes("ID", encoding='utf-8'))
        user_id= client.recv(1024).decode('utf-8')

        print(f"[{message_time}]{user_id} joined the server.")

        # Sending welcome message
        client_list.append(client)
        client.sendall(bytes(f"Welcome {user_id} to this TCP chatroom. You can type exit to leave.", encoding='utf-8'))

        # While loop to continually receive messages from client
        while True:
            try:
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

        # Shutdown client connection
        print(f"[{message_time}]{user_id} has left the chat.")
        client_list.remove(client)
        client.close()

# Allows server to write command line messages to client
def message_client(server):

    # While loop to continually send messages
    while True:
        # Get server message
        message_time = datetime.now().strftime("%H:%M")
        message = input()
        print(f"[{message_time}]Server: {message}")

        # Check for graceful exit
        if message.upper().strip() == "EXIT":
            print(f"[{message_time}]Server shutting down...")

            for client in client_list:
                try:
                    # Sending shut down message
                    client.sendall(bytes(f"[{message_time}]Server: {message}",encoding = 'utf-8'))
                    client.sendall(bytes(f"[{message_time}]Server shutting down...",encoding = 'utf-8'))
                    client.close()
                except:
                    pass

            # Shutting server down
            server.shutdown()
            server.server_close()
            break

        # Send message
        for client in client_list:
            try:
                client.sendall(bytes(f"[{message_time}]Server: {message}",encoding = 'utf-8'))
            except:
                break

if __name__ == "__main__":
    # Server creation message
    message_time = datetime.now().strftime("%H:%M")
    print(f"[{message_time}]Server created at port: {port_num}, host: {localhost}")

    # Starting server and starting thread for message_client
    server = socketserver.ThreadingTCPServer((localhost, port_num), TCPServer)
    threading.Thread(target=message_client, daemon = True, args = (server,)).start()
    server.serve_forever()