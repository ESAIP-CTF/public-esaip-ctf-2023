#! /usr/bin/env python3

from smartcard.System import readers
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.CardType import AnyCardType
from smartcard.ATR import ATR
from smartcard import util

WAIT_FOR_SECONDS = 5

def parse_keys_file(key_file):
    keys = []
    with open(key_file) as f:
        file_content = f.read().replace(" ", "").replace("\r", "").split("\n")
        for key in file_content:
            if key != "" and key[0] != "#":
                keys.append(key)
    return keys

def test_auth(conn, sector, key):
    # load key
    load_key = util.toBytes("FF 82 00 00 06 %s" % key)
    data, sw1, sw2 = conn.transmit(load_key)
    status = util.toHexString([sw1, sw2])

    # authenticate
    auth = util.toBytes("FF 86 00 00 05 01 00 %s 60 00" % util.toHexString([sector]))
    data, sw1, sw2 = conn.transmit(auth)
    status = util.toHexString([sw1, sw2])

    if status != "90 00":
        return False
    else:
        return True

def read_sector(conn, sector, key):
    sect = util.toHexString([sector * 4])
    # load key
    load_key = util.toBytes("FF 82 00 00 06 %s" % key)
    _, sw1, sw2 = conn.transmit(load_key)
    status = util.toHexString([sw1, sw2])

    # authenticate
    auth = util.toBytes("FF 86 00 00 05 01 00 %s 60 00" % sect)
    _, sw1, sw2 = conn.transmit(auth)
    status = util.toHexString([sw1, sw2])

    # get sector data
    sect = sector * 4
    data_ret = []
    for sec in range(sect, sect + 4):
        i = util.toHexString([sec])
        get_data = util.toBytes("FF B0 00 %s 10" % i)
        data, sw1, sw2 = conn.transmit(get_data)
        data_ret+= [util.toHexString(data)]
        status = util.toHexString([sw1, sw2])
        if status != "90 00":
            return False

    return data_ret

def write_sector(conn, sector, offset, data, key):
    if offset < 0 or offset > 2:
        return False

    sect = util.toHexString([sector * 4])
    # load key
    load_key = util.toBytes("FF 82 00 00 06 %s" % key)
    _, sw1, sw2 = conn.transmit(load_key)
    status = util.toHexString([sw1, sw2])

    # authenticate
    auth = util.toBytes("FF 86 00 00 05 01 00 %s 60 00" % sect)
    _, sw1, sw2 = conn.transmit(auth)
    status = util.toHexString([sw1, sw2])

    # get sector data
    sect = (sector * 4) + offset
    lenght = util.toHexString([16])

    sect = util.toHexString([sect])
    write_data = util.toBytes("FF D6 00 %s %s %s" % (sect, lenght, data))
    _, sw1, sw2 = conn.transmit(write_data)
    status = util.toHexString([sw1, sw2])
    if status != "90 00":
        return False
    else:
        return True

def get_coins(conn, key):
    try:
        if not test_auth(conn, 10, key):
            return -1
        data = read_sector(conn, 10, key)
        if(not data):
            return -1

        coins_temp = [bytes.fromhex(i) for i in data[0].split(" ")[6:10]]
        coins_bytes = b""
        for b in coins_temp:
            coins_bytes+= b
        coins = int.from_bytes(coins_bytes, byteorder='big')
        return coins
    except:
        return -1

def set_coins(conn, num, key):
    if num < 0:
        num = 0
    coins = [ord(l) for l in "coins:"]
    coins+= int(num).to_bytes(4, 'big')
    while len(coins) != 16:
        coins+= [0]

    return write_sector(conn, sector=10, offset=0, data=util.toHexString(coins), key=key)

if __name__ == '__main__':
    # respond to the insertion of any type of smart card
    card_type = AnyCardType()
    r = readers()
    print("\033[34;1m[+]\033[0;1m Reader: %s\033[0m" % r)

    # create the request. Wait for up to x seconds for a card to be attached
    request = CardRequest(timeout=WAIT_FOR_SECONDS, cardType=card_type)

    # listen for the card
    print("\033[34;1m[+]\033[0;1m Listening for card... (＿ ＿*) Z z z\033[0m", flush=True)
    service = None
    while service == None:
        try:
            service = request.waitforcard()
        except CardRequestTimeoutException:
            pass
            #print("ERROR: No card detected")
            #exit(-1)

    # when a card is attached, open a connection
    print("\033[34;1m[+]\033[0;1m Card attached (◕‿◕*)\033[0m")
    conn = service.connection
    conn.connect()

    print(get_coins(conn, "FF FF FF FF FF FF"))

