import select # for poll
import tincanchat
from types import SimpleNamespace
from collections import deque

HOST = tincanchat.HOST
PORT = tincanchat.PORT

clients = {}

def create_client(sock):
    """Return an object representing a client"""
    return SimpleNamespace(
        sock=sock,
        rest=bytes(),
        send_queue=deque()
    )

def broadcast_msg(msg):
    """ Add message to all connected clients' queues """
    data = tincanchat.prep_msg(msg)
    for client in clients.values():
        client.send_queue.append(data)
        poll.register(client.sock, select.POLLOUT)

if __name__ == '__main__':
    listen_sock = tincanchat.create_listen_socket(HOST, PORT)
    poll = select.poll()
    # registering a scoket passing the socket as an argument along with the type of activity we want the kernel to watch.
    # using POLLIN and POLLOUT to watch out for when a socket is ready to receive and send data respectively.
    poll.register(listen_sock, select.POLLIN)
    addr = listen_sock.getsockname()
    print(f"Listening on {addr}")

    # This is the event loop. Loop indefinitely, processing events
    # on all sockets when they occur
    while True:
        # Iterate over all sockets with events
        # poll.poll() returns a list of all the sockets that have become ready for us to work with.
        # For each socket, it also returns an event flag, which indicates the state of the socket.
        # This event flag tells whether we can read from(POLLIN) or write to the socket(POLLOUT),
        # or whether an error has occurred(POLLHUP, POLLERR, POLLNVAL)
        for fd, event in poll.poll():
            # clear-up a closed socket
            if event & (select.POLLHUP |
                        select.POLLERR |
                        select.POLLNVAL):
                poll.unregister(fd)
                del clients[fd]

            # Accept new connection, add client to clients dict
            elif fd == listen_sock.fileno():
                client_sock, addr = listen_sock.accept()
                client_sock.setblocking(False)
                fd = client_sock.fileno()
                clients[fd] = create_client(client_sock)
                poll.register(fd, select.POLLIN)
                print(f"Connection from {addr}")

            # Handle received data on socket
            elif event & select.POLLIN:
                client = clients[fd]
                addr = client.sock.getpeername()
                recvd = client.sock.recv(4096)
                if not recvd:
                    # the client state will get cleaned up in the
                    # next iteration of the event loop, as close()
                    # sets the socket to POLLNVAL
                    client.sock.close()
                    print(f"Client {addr} disconnected")
                    continue

                data = client.rest + recvd
                (msgs, client.rest) = tincanchat.parse_recvd_data(data)

                # If we have any messages, broadcast them to all clients
                for msg in msgs:
                    msg = f"{addr}: {msg}"
                    print(msg)
                    broadcast_msg(msg)
            
            # Send message to ready client
            elif event & select.POLLOUT:
                client = clients[fd]
                data = client.send_queue.popleft()
                sent = client.sock.send(data)
                if sent < len(data):
                    client.sends.appendleft(data[sent:])
                if not client.send_queue:
                    poll.modify(client.sock, select.POLLIN)


