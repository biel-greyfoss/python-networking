import socket
import ssl

from pprint import pprint


TARGET_HOST ='localhost'
TARGET_PORT = 8000
CA_CERT_PATH = 'example.crt'


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(CA_CERT_PATH)

    with socket.create_connection((TARGET_HOST, int(TARGET_PORT))) as sock:
        with context.wrap_socket(sock, server_hostname="example.com") as ssock:
            print(ssock.version())
            cert = ssock.getpeercert()
            print("Checking server certificate")
            pprint(cert)
            if not cert or ssl.match_hostname(cert, "example.com"):
                raise Exception(f"Invalid SSL cert for host {'example.com'}. Check if this is a man-in-the-middle attack!")
            print("Server certificate OK.\n Sending some custom request... GET ")
            ssock.send('GET / \n'.encode('utf-8'))
            print("Response received from server:")
            print(ssock.recv(1024).decode("utf-8"))
        