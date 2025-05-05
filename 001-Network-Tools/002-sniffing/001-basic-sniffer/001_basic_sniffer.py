#!/usr/bin/env python3
from scapy.all import sniff, IP
import sys

protocols = {6: "TCP", 17: "UDP", 1: "ICMP"}
count = 0

def process_packet(packet):
    global count
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        print(f"[+] {ip_layer.src} -> {ip_layer.dst} [{protocols.get(ip_layer.proto, 'Other')}]")
        count += 1

def main():
    global count
    try:
        time = int(input("Add a time limit for sniffing in minutes: "))
    except ValueError:
        sys.exit("Invalid time input.")

    filter_choice = input("Do you want the sniffer to print only TCP packets and ignore everything else? (Yes/No): ").strip().lower()

    if filter_choice == "yes":
        sniff(prn=process_packet, filter="tcp", timeout=(time * 60), store=False)
    elif filter_choice == "no":
        sniff(prn=process_packet, timeout=(time * 60), store=False)
    else:
        print("Invalid input! Defaulting to sniffing all packets.")
        sniff(prn=process_packet, timeout=(time * 60), store=False)
    
    print(f"[->] Packets captured: {count}")

if __name__ == "__main__":
    main()

