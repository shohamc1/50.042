import hashlib

with open("plain6.txt", "r") as f:
    plaintexts = f.read().split()

hashes = []

for plaintext in plaintexts:
    hashes.append(hashlib.md5(plaintext.encode()).hexdigest())

with open("salted6.txt", "w") as f:
    for item in hashes:
        f.write(f"{item}\n")
