import json
import math
import os
import socket
import time


def get_file_names(directory):
    file_names = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)) and (not filename.endswith('.png')) :
            file_names.append(filename)

    return file_names

def create_json_message(directory):
    file_names = get_file_names(directory)
    json_message = json.dumps({"chunks":file_names})
    return json_message


def udp_broadcast(message):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    sock.sendto(message.encode(), ("<broadcast>", 5001))

    # Close the socket
    sock.close()

def splitImage(name, directory):
    content_name = name
    filename = os.path.join(directory, content_name + '.png')
    c = os.path.getsize(filename)
    CHUNK_SIZE = math.ceil(math.ceil(c) / 5)

    index = 1
    with open(filename, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = os.path.join(directory, content_name + '_' + str(index))
            with open(chunkname, 'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
    print("Image split successfully into chunks.")


def chunk_announcer():
    userFileName= input("Enter file name to share:")
    direc="wholeimages"
    splitImage(userFileName, direc)
    print(f"Starting to announce {userFileName}.png, number of chunks:5")
    # Specify the directory you want to read the file names from

    # Create the JSON message with file names
    while True:
        message = create_json_message(direc)
        udp_broadcast(message)
        time.sleep(60)


if __name__ == '__main__':
    chunk_announcer()