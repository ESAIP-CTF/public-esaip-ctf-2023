from Crypto.Util.number import bytes_to_long
from multiprocessing import Process
from os import urandom
import socket

BANNER = b"""
__________                                /\        __________              
\______   \ ______  _  ________ __________)/ ______ \______   \ _______  ___
 |    |  _//  _ \ \/ \/ /  ___// __ \_  __ \/  ___/  |    |  _//  _ \  \/  /
 |    |   (  <_> )     /\___ \\\\  ___/|  | \/\___ \   |    |   (  <_> >    < 
 |______  /\____/ \/\_//____  >\___  >__|  /____  >  |______  /\____/__/\_ \\
        \/                  \/     \/           \/          \/            \/

        
"""

def read_line(s):
    body = b""
    while True:
        ch = s.recv(1)
        if ch == b"\n":
            break
        body = body + ch
    return body

def challenge(s):
    s.send(BANNER)
    s.send(b"What's the SBox you want to use for the encryption?\n")
    s.send(b"Example : 1,2,3,4,5,6...\n")

    try:
        sbox = read_line(s).decode()
        sbox = sbox.split(",")
        sbox = tuple([int(x) for x in sbox])
        assert len(sbox) == 256
    except:
        s.send(b"SBox is invalid!\n")
        exit()

    from aes import AES
    master_key = bytes_to_long(b"ECTF{AEEES_SBOX}")
    AES = AES(master_key, sbox)
    ciphertext = AES.encrypt(bytes_to_long(urandom(120)))

    s.send(b"Cipher text: " + str(ciphertext).encode() + b"\n")
    return

if __name__ == '__main__':
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 55555))
    s.listen(10)
    while True:
        client, addr = s.accept()
        print("Got connect from " + str(addr))
        p = Process(target=challenge, args=(client,))
        p.daemon = True
        p.start()
        client.close()