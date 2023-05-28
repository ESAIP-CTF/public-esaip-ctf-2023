from Cryptodome.Util.number import bytes_to_long, getPrime

FLAG = open("flag.txt", "rb").read()

def square(x, m, n=5):
    for _ in range(n):
        x = pow(x, 2, m)
    return x

def encrypt(flag):
    p = getPrime(1024)
    x = square(bytes_to_long(flag), p)
    return (x, p)

(X, P) = encrypt(FLAG)

print("X =", X)
print("P =", P)