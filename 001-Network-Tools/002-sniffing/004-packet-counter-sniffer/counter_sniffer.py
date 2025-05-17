#!/usr/bin/env python3
from scapy.all import sniff, IP
import time
import signal
import sys

protocol_count = {'TCP': 0, 'UDP': 0, 'ICMP': 0,'OTHER': 0}

running = True

def process_packet(packet):
    if packet.haslayer(IP):
        proto = packet[IP].proto
        if proto == 6:
            protocol_count['TCP'] += 1
        elif proto == 17:
            protocol_count['UDP'] += 1
        elif proto == 1:
            protocol_count['ICMP'] += 1
        else:
            protocol_count['OTHER'] += 1

def packet_count():
    print("[+] Packets count:")
    for proto, count in protocol_count.items():
        print(f"{proto}: {count}")
    print("*" * 40)

def handle_interrupt(signum, frame):
    global running
    running = False
    print("[!] Sniffing stopped.")
    packet_count()
    sys.exit(0)

def main():
    duration = input("Sniff time duration (0 = unlimited): ").strip()
    try:
        duration = int(duration)
    except ValueError:
        print("Invalid input. Using unlimited.")
        duration = 0

    signal.signal(signal.SIGINT, handle_interrupt)
    print("[*] Starting packet sniffing, Ctrl+C to stop.\n")

    start_time = time.time()

    while running:
        sniff(prn=process_packet, store=False, timeout=3)
        packet_count()

        progress = time.time() - start_time
        if duration > 0 and progress > duration:
            break


    packet_count()

if __name__ == "__main__":
    main()




