#!/usr/bin/env python

import argparse
import math
import sys


def main(args):
    # Number of Key Custodians
    nKC = args.nKC

    # Replication Factor
    rf = args.rf

    # Check the number of Key Custodians and Replication Factor, where 1<rf<nKC
    print("Number of Key Custodians: ", nKC)
    print("Replication Factor: ", rf)
    if rf <= 1 or rf >= nKC:
        print("Invalid Replication Factor of number of Key Custodians: 1<rf<nKC")
        sys.exit(1)

    # Read the secret from stdin
    secret = sys.stdin.readline()

    # Remove newlines from the secret
    secret = secret.replace("\n", "")
    secret = secret.replace("\r", "")

    # Remove headers and footers for OpenSSH Keys. Those are not secret.
    secret = secret.replace("-----BEGIN OPENSSH PRIVATE KEY-----", "")
    secret = secret.replace("-----END OPENSSH PRIVATE KEY-----", "")

    # print ("DEBUG: secret: " + secret)

    # Slice up the secret in approximately equal parts
    slices = []
    delimiter = math.ceil(len(secret) / nKC)
    for i in range(nKC):
        s = int(i * delimiter)
        e = int(i * delimiter + delimiter)
        # print ("DEBUG: s: ", s, " e: ", e)
        slices.append(secret[s:e])

    # Print the results split by each Key Custodian
    for i in range(nKC):
        print("\nSecret Slices for KC", i + 1)
        for s in range(rf):
            slicePos = (s + i) % nKC
            print("Secret Slice Slot", slicePos, ": ", slices[slicePos])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="N-Man Rule for Break Glass")
    parser.add_argument(
        "-k",
        "--key-custodians",
        type=int,
        default=3,
        dest="nKC",
        help="Number of Key Custodians",
    )
    parser.add_argument(
        "-r",
        "--replication-factor",
        type=int,
        default=2,
        dest="rf",
        help="Replication Factor",
    )

    main(parser.parse_args())
