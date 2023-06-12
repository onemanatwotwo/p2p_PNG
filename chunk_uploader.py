import json
import socket
from datetime import datetime

def chunk_uploader():
    def send_file(client_socket, filename):
        try:
            with open(filename, 'rb') as file:
                data = file.read()
                client_socket.sendall(data)
                print("File sent successfully:", filename)

                # Log the file's information
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_entry = f"{timestamp} - Chunk {filename} sent to {client_socket.getpeername()[0]}\n"
                log_file.write(log_entry)
        except IOError:
            print("Error: File not found:", filename)

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('0.0.0.0', 5000))

    # Listen for incoming connections
    server_socket.listen(1)

    print("Listening for connections on port 5000...")

    # Open the log file for writing
    log_file = open("UploadLog.txt", 'a')

    while True:
        # Accept a new connection
        client_socket, address = server_socket.accept()

        print("Received connection from:", address)

        # Receive the message from the client
        message = client_socket.recv(1048576).decode('latin-1')
        print(message)
        # Parse the JSON message
        try:
            json_data = json.loads(message)
            filename = json_data.get('requested_content')
            print(filename)
            if filename:
                send_file(client_socket, "wholeimages/" + filename)
            else:
                print("Error: Invalid JSON format")

        except json.JSONDecodeError:
            print("Error: Invalid JSON format")

        # Close the client socket
        client_socket.close()

    # Close the log file
    log_file.close()

if __name__ == '__main__':
    chunk_uploader()
