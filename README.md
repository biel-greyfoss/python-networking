# python-networking


Learning Python Network Programming

# chat-room
Requires:
* Clients connect to the server and then leave the connection open.
* Clients can continuously listen on connection and handle new messages sent by the server in one thread.
* Accepting user input and sending messages over the same connection in another thread.

Protocol:
1. Communication will be conducted over TCP.
2. The client will initiate a chat session by creating a socket connection to the server.
3. The server will accept the connection, listen for any messages from the client, and accept them.
4. The client will listen on the connection for any messages from the server, and accept them.
5. The server will send any messages from the client to all other connected clients.
6. Messages will be encoded in the UTF-8 character set for transmission, and they will be terminated by the null byte.