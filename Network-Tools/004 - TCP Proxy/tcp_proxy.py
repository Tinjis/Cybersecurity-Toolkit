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
