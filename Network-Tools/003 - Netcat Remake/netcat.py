import socket
import threading
import sys
import shlex
import subprocess
import textwrap
import argparse

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()
