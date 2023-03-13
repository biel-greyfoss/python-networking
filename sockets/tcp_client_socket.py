import socket
import sys

if __name__ == '__main__':
    try:
        # Socket family: AF_INET
        # Socket type: SOCK_STREAM (TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("Failed to create a socket")
        print(f"Reason: {err}")
        sys.exit()
    
    print("Socket created")

    #target_host = input("Enter the target host name to connect: ")
    #target_port = input("Enter the target port: ")
    # valid 
    # target_host, target_port = "www.bielcrystal.com", 443
    # invalid
    target_host, target_port = "www.dsfsacvdsvd.com", 443
    try:
        sock.connect((target_host, int(target_port)))
        print(f"Socket connected to {target_host} on port: {target_port}")
        sock.shutdown(2)
    except socket.error as err:
        print(f"Failed to connect to {target_host} on port: {target_port}")
        print(f"Reason: {err}")
        sys.exit()
