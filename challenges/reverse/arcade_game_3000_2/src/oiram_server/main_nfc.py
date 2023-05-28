#! /usr/bin/env python3

# nfc
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *
import mf1

# websocket
import asyncio
import threading
import websockets

cardinfos = ""

async def handler(websocket):
    global cardinfos
    print("client connected")
    cardinfos = ""
    while True:
        try:
            await websocket.recv()
            if len(cardinfos) > 0:
                await websocket.send(cardinfos)
                cardinfos = ""
        except:
            break
    print("client disconnected")

async def hello(websocket, path):
    async for data in websocket:
        print(f"Received: '{data}'")
        await websocket.send(data)

def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws_server = websockets.serve(handler, "localhost", 8768)

    loop.run_until_complete(ws_server)
    loop.run_forever()
    loop.close()

class transmitobserver(CardObserver):
    def __init__(self):
        pass

    def update(self, observable, actions):
        global cardinfos
        (addedcards, removedcards) = actions
        type = ""
        card = None
        for card_t in addedcards:
            card = card_t
            type = "added"
            break
        if card == None:
            for card_t in removedcards:
                card = card_t
                type = "removed\n"
                break
        if card == None:
            return
        
        if type == "removed":
            print("-Removed")
            return
        # Create connection to card
        try:
            card.connection = card.createConnection()
            card.connection.connect()
            conn = card.connection
        except:
            return

        # get and print the UID of the card
        get_uid = toBytes("FF CA 00 00 00")
        data, sw1, sw2 = conn.transmit(get_uid)
        uid = toHexString(data)
        print("+Inserted: %s" % uid)

        if not mf1.test_auth(conn, 10, "FF FF FF FF FF FF"):
            return False
        coins = mf1.get_coins(conn, "FF FF FF FF FF FF")
        if coins == -1:
            return False
        print("coins: %d" % coins)
        if coins >= 100:
            mf1.set_coins(conn, coins - 100, "FF FF FF FF FF FF")
        cardinfos = '{"card": "%s", "coins": %d}' % (uid, coins)
        #mf1.set_coins(conn, 999999999, "FF FF FF FF FF FF")


if __name__ == '__main__':
    print("Press Enter to exit program")
    cardmonitor = CardMonitor()
    cardobserver = transmitobserver()
    cardmonitor.addObserver(cardobserver)

    try:
        server = threading.Thread(target=between_callback, daemon=True)
        server.start()
    except KeyboardInterrupt:
        pass

    input()
