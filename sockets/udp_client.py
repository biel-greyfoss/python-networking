from socket import socket, AF_INET, SOCK_DGRAM

MAX_SIZE = 4096
PORT = 12345

if __name__ == '__main__':
    sock = socket(AF_INET,SOCK_DGRAM)
    msg = "Hello UDP server"
    sock.sendto(msg.encode(),('', PORT))
    data, addr = sock.recvfrom(MAX_SIZE)
    print("Server says:")
    print(repr(data))