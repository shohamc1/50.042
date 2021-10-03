import csv
import requests
import urllib3

urllib3.disable_warnings()

with open("hashes_clean.txt") as f:
    hashes = f.read().split()

answer = {}

for hash in hashes:
    try:
        print(hash)
        response = requests.get(f"https://www.nitrxgen.net/md5db/{hash}", verify=False)
        answer[hash] = response.text
    except:
        print(f"Error with hash {hash}")

with open("solution.csv", "w") as f:
    w = csv.writer(f)
    w.writerows(answer.items())
