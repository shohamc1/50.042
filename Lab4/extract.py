#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

import argparse


def getInfo(headerfile):
    with open(headerfile, "rb") as f:
        header = f.read()
        return header, len(header)


def extract(infile, outfile, headerfile):
    header, header_len = getInfo(headerfile)
    freq_dict = {}

    with open(infile, "rb") as f:
        skip_blocks = int((header_len / 8) + 1)  # bytes
        f.read(skip_blocks * 8)  # skip reading header

        while True:
            byte = f.read(8)
            if not byte:
                break
            else:
                freq_dict[byte] = freq_dict.get(byte, 0) + 1

    most_common_block = max(freq_dict, key=freq_dict.get)

    with open(infile, "rb") as source, open(outfile, "wb") as destination:
        skip_blocks = int((header_len / 8) + 1)  # bytes
        source.read(skip_blocks * 8)  # skip reading header
        destination.write(header + b"\n")

        while True:
            byte = source.read(8)
            if not byte:
                break

            if byte == most_common_block:
                write_byte = b"00000000"
            else:
                write_byte = b"11111111"
            destination.write(write_byte)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract PBM pattern.")
    parser.add_argument("-i", dest="infile", help="input file, PBM encrypted format")
    parser.add_argument("-o", dest="outfile", help="output PBM file")
    parser.add_argument("-hh", dest="headerfile", help="known header file")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    headerfile = args.headerfile

    print("Reading from: %s" % infile)
    print("Reading header file from: %s" % headerfile)
    print("Writing to: %s" % outfile)

    success = extract(infile, outfile, headerfile)
