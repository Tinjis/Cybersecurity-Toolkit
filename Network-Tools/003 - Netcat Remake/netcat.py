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
    
    cmd_list = shlex.split(cmd)
    output = subprocess.check_output(cmd_list, stderr=subprocess.STDOUT)
    return output.decode()
