import json
import socket



def content_discovery():
    ip_address = '0.0.0.0'  # Use '0.0.0.0' to listen on all available network interfaces
    port = 5001  # Specify the port number you want to listen on


    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.bind((ip_address,port))

    content_dictionary={}
    # Listen for incoming data
    while True:
        data, addr = sock.recvfrom(1024)  # Receive data with maximum buffer size of 1024 bytes
        print(f"Received data from {addr}")

        # Parse the JSON message
        try:
            json_data = json.loads(data.decode('latin-1'))
            # Process the parsed JSON data as needed
            print("Parsed JSON data:", json_data)
            for chunk_name in json_data['chunks']:
                if chunk_name not in content_dictionary:

                    content_dictionary[chunk_name] = []
                if addr[0] not in content_dictionary[chunk_name]:
                    content_dictionary[chunk_name].append(addr[0])

            print("Content Dictionary:", content_dictionary)
            with open('content_dictionary.json', 'w') as fp:
                json.dump(content_dictionary,fp)

        except json.JSONDecodeError as e:
            print("Error parsing JSON:", str(e))
        # Get the UDP broadcast sender's IP address


if __name__ == '__main__':
    content_discovery()