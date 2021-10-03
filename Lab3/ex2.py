import hashlib
import itertools

plaintext_list = []
hashed_list = []

char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
char_set = [char for char in char_set]
char_length = 5

with open("hash5.txt", "r") as f:
    hashes = f.read()
    hashes = hashes.split()

iter_set = list(itertools.product(char_set, repeat=char_length))

for permutation in iter_set:
    plain = "".join(permutation)
    hashed = hashlib.md5(plain.encode()).hexdigest()
    if hashed in hashes:
        print(f"Plain: {plain}\tHash: {hashed}")
