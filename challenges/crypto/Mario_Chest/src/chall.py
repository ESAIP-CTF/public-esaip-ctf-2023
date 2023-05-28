
import random
from decimal import Decimal,getcontext
from multiprocessing import Process
import socket

getcontext().prec = 80


FLAG = "ECTF{WhEn_Mari0_W4nTs_To_Share}"

# Menu
menu_options = {
    "1": 'Get the secret',
    "2": 'Create new share',
    "3": 'Exit',
}

banner = b"""
                     _                              
 _____         _    | |       _____ _           _   
|     |___ ___|_|___|_|___   |     | |_ ___ ___| |_ 
| | | | .'|  _| | . | |_ -|  |   --|   | -_|_ -|  _|
|_|_|_|__,|_| |_|___| |___|  |_____|_|_|___|___|_|  
                                                                                                                                                                  
"""

# Print menu
def print_menu(s):
    for key in menu_options.keys():
        menu = key+ '--'+menu_options[key] 
        s.send(menu.encode()+b"\n")


# Get user input
def read_line(s):
    body = b""
    while True:
        ch = s.recv(1)
        if ch == b"\n":
            break
        body = body + ch
    return body

def str_to_int(secret):
    return sum([ord(c) * (256 ** i) for i, c in enumerate(secret)])

def int_to_str(secret_int):
    secret_str = []
    while secret_int > 0:
        secret_str.append(chr(secret_int % 256))
        secret_int //= 256
    return ''.join(secret_str)

def create_point(x):
    a = int(str(6**3)[1:] + str(5**4)[:2])
    b = int(str(3**3)[1:] + str(4**4)[1:])
    c = a * b
    return x - c


def create_share(x,m,secret):

    coefficients = coeff(m, secret)
    shares.append((x, polynom(x, coefficients)))
         

def reconstruct_secret(shares):
    sums = 0
 
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)
 
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi)/(xi-xj))
 
        prod *= yj
        sums += Decimal(prod)
 
    return int(round(Decimal(sums), 0))
 
 
def polynom(x, coefficients):
    point = 0

    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point
 
 
def coeff(t, secret):
    coeff = [random.randrange(0, 10**5) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff
 
 
def generate_shares(n, m, secret):
    coefficients = coeff(m, secret)
    shares = []
 
    for _ in range(1, n+1):
        x = random.randrange(1, 10**5)
        shares.append((x, polynom(x, coefficients)))
 
    return shares
 

def verify_secret(generated_secret):
    if generated_secret == FLAG:

        return f"Okey, I'll share my secret with you : {FLAG}"
    else :
        return "I won't share my secret if you won't share yours ( ͡° ͜ʖ ͡°)"

# Challenge
def challenge(s):
    s.send(banner)
    while (True):
        print_menu(s)
        choice = read_line(s)
        if choice.decode("utf-8") == "1":
            pool = []
            pool.append(shares[-1])
            pool.append(shares[-2])
            reconstructed = int_to_str(reconstruct_secret(pool))
            result =  verify_secret(reconstructed)
            s.send(result.encode()+b"\n")

        elif choice.decode("utf-8") == "2":
            s.send(b"Enter your new share ID number : \n")
            ID = read_line(s)
            point = int(ID)
            create_share(create_point(point),t,secret_int)
            
        elif choice.decode("utf-8") == "3":
            break
        else:
            s.send(b"Wrong choice: send 1,2 or 3\n")

 
# Main
if __name__ == '__main__':

    t, n = 5, 10
    secret_int = str_to_int(FLAG)
    shares = generate_shares(n, t, secret_int)

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