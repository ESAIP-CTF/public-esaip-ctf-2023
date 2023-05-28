import itertools

def dechiffrement_cesar(chiffre, cle):
    message = ""
    for caractere in chiffre:
        if caractere.isalpha():
            decalage = cle % 26
            if caractere.islower():
                message += chr((ord(caractere) - ord('a') - decalage) % 26 + ord('a'))
            else:
                message += chr((ord(caractere) - ord('A') - decalage) % 26 + ord('A'))
        else:
            message += caractere
    return message

def dechiffrage_cesar_cle_variable(chiffre, cles_possibles, n):
    message = ""
    for i, caractere in enumerate(chiffre):
        cle = cles_possibles[i % n]
        message += dechiffrement_cesar(caractere, cle)
    return message

def essayer_cles_possibles(chiffre, premiers_caracteres_clairs, n):
    premiers_caracteres_chiffres = chiffre[:n]
    for combinaison_cles in itertools.product(range(26), repeat=n):
        message_dechiffre = dechiffrage_cesar_cle_variable(premiers_caracteres_chiffres, combinaison_cles, n)
        if message_dechiffre.startswith(premiers_caracteres_clairs):
            return combinaison_cles
    return None

message_chiffre = "QVWQ{0q3_ELefe3_ShXxN4_4_MkP_MdDf3}"
premiers_caracteres_clairs = "ECTF"
n = 4

cles_possibles = essayer_cles_possibles(message_chiffre, premiers_caracteres_clairs, n)
if cles_possibles:
    print(f"Clés possibles : {cles_possibles}")
    message_dechiffre = dechiffrage_cesar_cle_variable(message_chiffre, cles_possibles, n)
    print(f"Message déchiffré : {message_dechiffre}")
else:
    print("Aucune combinaison de clés n'a été trouvée.")
