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


valid_alphabet = list(string.printable)
lower_limit = 1
upper_limit = len(valid_alphabet) - 1


def shift(filein: string, fileout: string, key: int):
    output = []
    with open(filein, mode="r", newline="\n") as f:
        text = f.read()
        for char in text:
            cindex = valid_alphabet.index(
                char
            )  # character index in string.printable array
            new_cindex = (cindex + key) % len(valid_alphabet)
            output.append(valid_alphabet[new_cindex])

    with open(fileout, mode="w", newline="\n") as f:
        f.write("".join(output))


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument(
        "-k",
        dest="key",
        help="key (int between {} and {})".format(lower_limit, upper_limit),
    )
    parser.add_argument("-m", dest="mode", help="mode ('e' or 'd')")

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
