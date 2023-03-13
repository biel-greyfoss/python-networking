import socket

from time import ctime

HOST = 'localhost'
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    # backlog: 5 specifies the number of unaccepted connections that the system will allow before refusing new connections
    server_socket.listen(5)
    # the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while True:
        print("Server waiting for connection...")
        client_sock, addr = server_socket.accept()
        print(f"Client connected from: {addr}")

        while True:
            data = client_sock.recv(BUFSIZ)
            if not data or data.decode("utf-8") == 'END':
                break
            
            print(f"Received from client: {data.decode('utf-8')}")
            print(f"Sending the server time to client: {ctime()}")
            try:
                client_sock.send(bytes(ctime(), "utf-8"))
            except KeyboardInterrupt:
                print("Exited by user")
        
        client_sock.close()
    
    server_socket.close()

