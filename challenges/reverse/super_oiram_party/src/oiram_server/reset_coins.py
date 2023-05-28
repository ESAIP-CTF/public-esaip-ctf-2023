#! /usr/bin/env python3

# nfc
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *
import mf1

class transmitobserver(CardObserver):
    def __init__(self):
        pass

    def update(self, observable, actions):
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
                type = "removed"
                break
        if card == None:
            return
        
        if type == "removed":
            print("-Removed\n")
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

        # RESET CARD COINS
        if not mf1.test_auth(conn, 10, "FF FF FF FF FF FF"):
            return False
        coins = mf1.get_coins(conn, "FF FF FF FF FF FF")
        if coins == -1:
            print("Failed to get coins/card not initialized")
        print("Coins: %s" % coins)
        if coins != 50:
            if mf1.set_coins(conn, 50, "FF FF FF FF FF FF"):
                print("Coins reset to 50")
            else:
                print("Failed to reset coins")
        else:
            print("No reset needed")


if __name__ == '__main__':
    print("Press Enter to exit program")
    cardmonitor = CardMonitor()
    cardobserver = transmitobserver()
    cardmonitor.addObserver(cardobserver)

    input()