import threading
from socket import *
import os
import mimetypes

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        if not message:
            connectionSocket.close()
            return

        filename = message.split()[1]

        file_path = './' + filename

        try:
            with open(file_path, 'rb') as file:
                response_body = file.read()
            response_header = 'HTTP/1.1 200 OK\r\n'
            content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        except FileNotFoundError:
            response_body = b"404 Not Found"
            response_header = 'HTTP/1.1 404 Not Found\r\n'
            content_type = 'text/html'

        response_header += f'Content-Length: {len(response_body)}\r\n'
        response_header += f'Content-Type: {content_type}\r\n\r\n'
        
        connectionSocket.sendall(response_header.encode() + response_body)
    finally:
        connectionSocket.close()

def main():
    serverPort = 6789
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)
    print("The server is ready to receive")
    while True:
        connectionSocket, addr = serverSocket.accept()
        threading.Thread(target=handle_client, args=(connectionSocket,)).start()

if __name__ == "__main__":
    main()