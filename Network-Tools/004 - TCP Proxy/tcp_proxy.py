import sys
import socket
import threading


HEX_FILTER = ""

for i in range(256):
    char = chr(i)

    if len(repr(char)) == 3:
        HEX_FILTER += char

    else:
        HEX_FILTER += "."

def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()

    for i in range(0, len(src), length):
        word = str(src[i : i+length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])

        hexwidth = length * 3
        
        results.append(f"{i:04x} {hexa:<{hexwidth}} {printable}")

    if show:
        for line in results:
            print(line)
    else:
        return results
