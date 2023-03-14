import threading
import tincanchat


HOST = tincanchat.HOST
PORT = tincanchat.PORT

def handle_client(sock, addr):
    """ Receive one message and echo it back to client, then close socket """    
    try:
        msg = tincanchat.recv_msg(sock)

        msg = f"{addr}:{msg}"
        print(msg)
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
        # Thread will run function handle_client() autonomously
        # and concurrently to this while loop
        thread = threading.Thread(target=handle_client, args=[client_sock, addr], daemon=True)
        thread.start()

        print(f'Connection from {addr}')
