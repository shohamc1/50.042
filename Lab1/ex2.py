#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


# Import libraries
import argparse
import string
import enum


class Mode(enum.Enum):
    ENCRYPT = "e"
    DECRYPT = "d"


lower_limit = 1
upper_limit = 255


def shift(filein: string, fileout: string, key: int):
    output = bytearray()
    with open(filein, mode="rb") as f:
        text = bytearray(f.read())

    for byte in text:
        output += bytearray([(byte + key) % (upper_limit + 1)])

    with open(fileout, mode="wb") as f:
        f.write(output)


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument("-k", dest="key", help="key")
    parser.add_argument("-m", dest="mode", help="'e' or 'd'")

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = int(args.key)
    mode = Mode(args.mode)

    if not 1 <= key <= len(string.printable) - 1:
        raise ValueError("key not in valid range.")

    if mode == Mode.ENCRYPT:
        shift(filein, fileout, key)
    else:
        shift(filein, fileout, key * -1)
