def chiffrement_cesar(message, cle):
    chiffre = ""
    for caractere in message:
        if caractere.isalpha():
            decalage = cle % 26
            if caractere.islower():
                chiffre += chr((ord(caractere) - ord('a') + decalage) % 26 + ord('a'))
            else:
                chiffre += chr((ord(caractere) - ord('A') + decalage) % 26 + ord('A'))
        else:
            chiffre += caractere
    return chiffre


def chiffrement_cesar_cle_variable(message, n):
    cle_base = [12, -7, 3, -15, 20, -8]  # Vous pouvez modifier les valeurs de cette liste pour changer les clés
    chiffre = ""
    for i, caractere in enumerate(message):
        cle = cle_base[i % n]
        chiffre += chiffrement_cesar(caractere, cle)
    return chiffre


message_original = "ECTF{0n3_LIttl3_GoUmB4_4_ThE_TaSt3}"
n = 4

message_chiffre = chiffrement_cesar_cle_variable(message_original, n)
print("Message chiffré :", message_chiffre)