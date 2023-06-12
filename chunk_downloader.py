import json
import os
import shutil
import socket



def stitchImageBack(name, directory):
    chunk_filenames = [os.path.join(directory, name + '_' + str(i)) for i in range(1, 6)]
    output_filename = os.path.join(directory, name + '.png')

    # Create a temporary directory for processing
    temp_directory = os.path.join(directory, 'temp')
    os.makedirs(temp_directory, exist_ok=True)

    try:
        # Combine the chunks into a single file
        with open(output_filename, 'wb') as output_file:
            for chunk_filename in chunk_filenames:
                with open(chunk_filename, 'rb') as chunk_file:
                    shutil.copyfileobj(chunk_file, output_file)

        print('Chunks stitched successfully into:', output_filename)

        # Remove the individual chunk files

    except Exception as e:
        print('Error stitching the chunks:', str(e))

    finally:
        # Remove the temporary directory
        os.rmdir(temp_directory)

def chunk_downloader():
    file_name = input("Enter the file name: ")

    port = 5000

    with open('content_dictionary.json') as json_file:
        content_dictionary = json.load(json_file)
    for i in range(1, 6):
        ip_addresses = content_dictionary[file_name + "_" + str(i)]

        payload = {"requested_content": file_name + "_" + str(i)}
        json_payload = json.dumps(payload)
        for ip_address in ip_addresses:
            print(ip_address)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # Connect to the server
                client_socket.connect((ip_address, port))
                # Send the JSON payload to the server
                client_socket.sendall(json_payload.encode('latin-1'))
                received_chunk = client_socket.recv(1048576)
                if not received_chunk:
                    continue
                chunk_filename = f"wholeimages/{file_name}_{str(i)}"
                with open(chunk_filename, "wb") as file:
                    file.write(received_chunk)
                print("Chunk", i, "received successfully:", chunk_filename)
            except ConnectionRefusedError:
                print("Connection refused to", ip_address)
            finally:
                client_socket.close()
    stitchImageBack(file_name,"wholeimages")
if __name__ == '__main__':
    chunk_downloader()