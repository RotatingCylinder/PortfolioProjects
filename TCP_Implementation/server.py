import socketserver
import threading
import sys

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
    def handle(self):
        client = self.request

        # While loop to continually receive messages from client
        while True:

            # If client is new, add to client_list and give welcome message
            if self.client_address not in client_list:
                client_list.append(self.client_address)
                client.sendall(bytes("Welcome to this TCP chatroom. You can type exit to leave.", encoding='utf-8'))
                print(f"{self.client_address} joined the server.")
                continue

            # Receive and print next message from client
            message = client.recv(1024).decode('utf-8')
            print(f"{self.client_address} sent: {message}")

            # Check for graceful exit
            if message.strip().upper() == "EXIT":
                client.sendall(bytes("Exiting server...",encoding = 'utf-8'))
                break

        # If while loop is exited, then server has stopped receiving messages and is shutting down
        # MUST CHANGE FOR MULTI-CLIENT IMPLEMENTATION
        print("Server shutting down...")
        sys.exit()

if __name__ == "__main__":

    # With statement ensures resources allocated to socketserver are released
    with socketserver.TCPServer((localhost, port_num), Server) as server:
        print(f"Server started at port: {port_num}, host: {localhost}")
        server.serve_forever() # Starts the server
        handle_thread = threading.Thread(target=Server.handle) # Thread for handle
        handle_thread.start()
