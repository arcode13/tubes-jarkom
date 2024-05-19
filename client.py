import sys
from socket import *

def main():
    if len(sys.argv) != 4:
        print("Cara Run : client.py <server_ip> 6789 index.html")
        sys.exit(1)

    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    filePath = sys.argv[3]

    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        request = f"GET {filePath} HTTP/1.1\r\nHost: {serverName}:{serverPort}\r\n\r\n"
        clientSocket.send(request.encode())

        response = b""
        while True:
            chunk = clientSocket.recv(1024)
            if not chunk:
                break
            response += chunk

        print(response.decode())
    finally:
        clientSocket.close()

if __name__ == "__main__":
    main()
