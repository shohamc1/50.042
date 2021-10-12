#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS


from present import *
import argparse

nokeybits = 80
blocksize = 64
blocksize_bytes = 8


def ecb(infile, outfile, key, mode):
    with open(infile, "rb") as source, open(outfile, "wb") as destination:
        result = []
        if mode == 1:
            while True:
                byte = source.read(blocksize_bytes)
                if not byte:
                    break

                encrypted = encrypt_blocks(byte, key)
                destination.write(encrypted.to_bytes(8, byteorder="big"))
        elif mode == 0:
            while True:
                byte = source.read(blocksize_bytes)
                if not byte:
                    break

                decrypted = decrypt_blocks(byte, key)
                result.append(decrypted)

            # remove padding
            result[-1], writingbits = remove_padding(result[-1])

            for i in range(len(result) - 1):
                destination.write(result[i].to_bytes(8, byteorder="big"))
            destination.write(result[-1].to_bytes(writingbits, byteorder="big"))


def decrypt_blocks(plain, key):
    int_format = int.from_bytes(plain, byteorder="big")
    return present_inv(int_format, key)


def encrypt_blocks(plain, key):
    if len(plain) < blocksize_bytes:
        # padding is required, PKCS7 format

        padding_size = blocksize_bytes - len(plain)
        plain += bytes(padding_size for _ in range(padding_size))

    int_format = int.from_bytes(plain, byteorder="big")
    return present(int_format, key)


def remove_padding(block):
    pad = block & 0xFF

    if pad > 0x10:
        # no padding
        return block, 8
    for i in range(pad):
        # check if it is padding
        temp = (block >> 8 * i) & 0xFF
        if temp != pad:
            return block, 8

    block = block >> 8 * pad
    return block, 8 - pad


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Block cipher using ECB mode.")
    parser.add_argument("-i", dest="infile", help="input file")
    parser.add_argument("-o", dest="outfile", help="output file")
    parser.add_argument("-k", dest="key", help="key, any integer")
    parser.add_argument("-m", dest="mode", help="mode")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    key = args.key
    mode = args.mode

    if mode.lower() == "e":
        ecb(infile, outfile, int(key), 1)
    else:
        ecb(infile, outfile, int(key), 0)
