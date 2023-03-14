import threading
from queue import Queue
import socket
import tincanchat

HOST = tincanchat.HOST
PORT = tincanchat.PORT

send_queues = {}
lock = threading.Lock()

def handle_client_recv(sock: socket, addr: str):
    """ Receive messages from client and broadcast them to
        other clients until client disconnects """
    rest = bytes()
    while True:
        try:
            (msgs, rest) = tincanchat.recv_msgs(sock, rest)
        except (EOFError, ConnectionError):
            handle_disconnect(sock, addr)
            break
        for msg in msgs:
            msg = f"{addr}: {msg}"
            print(msg)
            broadcast_msg(msg)

def handle_client_send(sock: socket, q: Queue, addr: str):
    """ Monitor queue for new messages, send them to client as
        they arrive """
    while True:
        msg = q.get() # block until returned
        if msg is None:
            break
        try:
            tincanchat.send_msg(sock, msg)
        except (ConnectionError, BrokenPipeError):
            handle_disconnect(sock ,addr)
            break

def broadcast_msg(msg: str):
    """ Add message to each connected client's send queue """
    with lock:
        for q in send_queues.values():
            q.put(msg)


def handle_disconnect(sock: socket, addr: str):
    """ Ensure queue is cleaned up and socket closed when a client
        disconnects """
    fd = sock.fileno()
    with lock:
        # Get send queue for this client
        q = send_queues.get(fd, None)

    # If we find a queue then this disconnect has not yet been handled
    if q:
        q.put(None)
        del send_queues[fd]
        addr = sock.getpeername()
        print(f"Client {addr} disconnected")
        sock.close()

if __name__ == "__main__":
    listen_sock = tincanchat.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print(f"Listening on {addr}")

    while True:
        client_sock, addr = listen_sock.accept()

        q = Queue() # create a queue for each send thread
        with lock:
            send_queues[client_sock.fileno()] = q # store the queue in the send_queues dict
        
        # using two threads per client
        recv_thread = threading.Thread(target=handle_client_recv, args=[client_sock, addr], daemon=True)

        send_thread = threading.Thread(target=handle_client_send, args=[client_sock, q, addr], daemon=True)


        recv_thread.start()
        send_thread.start()
        print(f"Connection from {addr}")