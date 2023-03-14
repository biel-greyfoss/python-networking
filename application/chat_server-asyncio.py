import asyncio
from asyncio import transports
import tincanchat

HOST = tincanchat.HOST
PORT = tincanchat.PORT
clients = [] # save clients that can broadcast to

class ChatServerProtocol(asyncio.Protocol):
    """
    Each instance of class represents a client and the socket 
       connection to it.
    """
    def connection_made(self, transport: transports.BaseTransport) -> None:
        """ Called on instantiation, when new client connects 
            Equals to socket.accept()
        """
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self._rest = b''
        clients.append(self) 
        print(f"Connection from {self.addr}")

    def data_received(self, data: bytes) -> None:
        """ Handle data as it's received. Broadcast complete messages to all other clients 
            Equals to poll.poll() returning a POLLIN event and recv() on the socket
        """
        data = self._rest + data
        (msgs, rest) = tincanchat.parse_recvd_data(data)
        self._rest = rest
        for msg in msgs:
            msg = msg.decode("utf-8")
            msg = f"{self.addr}: {msg}"
            print(msg)
            msg = tincanchat.prep_msg(msg)
            for client in clients:
                client.transport.write(msg) # non-blocking

    def connection_lost(self, exc: Exception | None) -> None:
        """ Called on client disconnect. Clean up client state 
            Equals to socket.recv() returning an empty result or a ConnectionError
        """
        print(f"Client {self.addr} disconnected")
        clients.remove(self)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)   
     # Create server and initialize on the event loop
    coroutine = loop.create_server(ChatServerProtocol,
                                   host=HOST,
                                   port=PORT)
    # init the server
    server = loop.run_until_complete(coroutine)
    # print listening socket info
    for socket in server.sockets:
        addr = socket.getsockname()
        print(f"Listenting on {addr}")
    
    # Run the loop to process client connections
    loop.run_forever()