from multiprocessing import Process
import socket


# Get user input
def read_line(s):
    body = b""
    while True:
        ch = s.recv(1)
        if ch == b"\n":
            break
        body = body + ch
    return body


def challenge(s):
    s.send(b"What's your number? ")
    num = read_line(s).decode()

    if not num < "0":
        s.send(b"Invalid number.\n")
        exit()

    num = float(num)
    if not num > float("0"):
        s.send(b"Invalid number.\n")
        exit()

    num = int(num)
    if not num == int("0"):
        s.send(b"Invalid number.\n")
        exit()

    s.send(b"Well done: ECTF{FAKE_FLAG}")
    return


# Main
if __name__ == '__main__':
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 55555))
    s.listen(10)
    while True:
        client, addr = s.accept()
        print(f"Got connect from {addr}")
        p = Process(target=challenge, args=(client,))
        p.daemon = True
        p.start()
        client.close()
