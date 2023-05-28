from Cryptodome.Util.number import long_to_bytes

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        r = pow(n, (p + 1) // 4, p)
        return (r, p - r)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    

    return (r, p - r)


def decrypt(x, p, n=5):
    if n == 0:
        d = long_to_bytes(x)
        if b"ECTF" in d:
            print("Flag =", d.decode())
    else:
        x1, x2 = tonelli(x, p)

        try:
            decrypt(x1, p, n - 1)
        except AssertionError:
            pass

        try:
            decrypt(x2, p, n - 1)
        except AssertionError:
            pass

if __name__ == "__main__":
    decrypt(
        65567906504707001412451629380105920336765646875361267702392177389975788601105395041727677960531694075172671673825534663404646697891108703571487714370157822718820383082425198093895770956243411362693772945081793898878903728208012455412074768926681046872056914503511397246233621635857399405920045067524154745070,
        126419363563553215091646637314497854198261588036382180640893319022541659598027100223880826774071842687403022731516037083359599621020514054284689589273154786802636897124000251303336410620757242551598664334914370563254424053331496101404625326501881265007678722518697084930349838815078675100361385273502712083087
    )