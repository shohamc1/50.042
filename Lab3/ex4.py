from random import choice
import hashlib

charset = "abcdefghijklmnopqrstuvwxyz"

plain = [
    "aseas",
    "cance",
    "di5gv",
    "dsmto",
    "egunb",
    "hed4e",
    "lou0g",
    "mlhdi",
    "nized",
    "ofror",
    "opmen",
    "owso9",
    "sso55",
    "tpoin",
    "tthel",
]

salted_array = []
hashed_array = []

for entry in plain:
    salt = choice(charset)
    salted = entry + salt
    hashed = hashlib.md5(salted.encode()).hexdigest()

    salted_array.append(salted)
    hashed_array.append(hashed)

with open("plain6.txt", "w") as f:
    f.write("\n".join(salted_array))

with open("salted6.txt", "w") as f:
    f.write("\n".join(hashed_array))
