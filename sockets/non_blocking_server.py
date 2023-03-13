import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.settimeout(0.5)
    sock.bind(("127.0.0.1", 0))

    socket_address =sock.getsockname()
    print(f"Asynchronous socket server launched on socket: {socket_address}")
    while(1):
        sock.listen(1)