import socket
import ssl

SSL_SERVER_PORT = 8000

"""
# Generated self-signed SSL certificate by the command below:

openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
  -keyout example.key -out example.crt -subj "/CN=example.com" \
  -addext "subjectAltName=DNS:example.com,DNS:www.example.net,IP:10.0.0.1"
"""

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("example.crt", "example.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('', SSL_SERVER_PORT))
        sock.listen(5)
        print(f"Waiting for ssl client on port {SSL_SERVER_PORT}")

        with context.wrap_socket(sock, server_side=True) as ssock:
            conn, addr = ssock.accept()


            # Generate your server's  public certificate and private key pairs.
            print(conn.read())
            conn.write('200 OK\r\n\r\n'.encode())
            print("Served ssl client. Exiting...")