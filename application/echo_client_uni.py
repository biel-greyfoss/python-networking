import sys, socket
import tincanchat

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = tincanchat.PORT

if __name__ == '__main__':
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            print(f"\nConnected to {HOST}:{PORT}")
            print("Type message, enter to send, 'q' to quit")
            msg = input()
            if msg == 'q':
                break

            tincanchat.send_msg(sock, msg) # Blocks until sent
            print(f"Sent message: {msg}")

            msg = tincanchat.recv_msg(sock)

            print("Received echo:" + msg)
        except ConnectionError:
            print('Socket error')
            break
        finally:
            sock.close()
            print('Closed connection to server\n')

