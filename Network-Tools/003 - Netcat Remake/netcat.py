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
