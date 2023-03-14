import tincanchat

HOST = tincanchat.HOST
PORT = tincanchat.PORT

def handle_client(sock, addr):
    """ Receive data from the client via sock and echo it back """
    try:
        msg = tincanchat.recv_msg(sock)

        print(f"{addr}:{msg}")
        tincanchat.send_msg(sock, msg)
    except (ConnectionError, BrokenPipeError):
        print('Socket error')
    finally:
        print(f'Closed connection to {addr}')
        sock.close()

if __name__ == '__main__':
    listen_sock = tincanchat.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print(f"Listening on {addr}")

    while True:
        client_sock, addr = listen_sock.accept()
        print(f'Connection from {addr}')

        handle_client(client_sock, addr)
