import socket

HOST = "localhost"
PORT = 12345
BUFSIZ = 4096
ADDR = (HOST, PORT)

if __name__ == '__main__':
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(ADDR)

    payload = "GET TIME"

    try:
        while True:
            client_sock.send(payload.encode('utf-8'))
            data = client_sock.recv(BUFSIZ)
            print(repr(data))

            more = input("Want to send more data to server[y/n] :")
            if more.lower() == 'y':
                payload = input("Enter payload: ")
            else:
                break
    except KeyboardInterrupt:
        print("Exited by user")

    client_sock.close()