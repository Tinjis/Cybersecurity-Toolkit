#!/usr/bin/env python3
from scapy.all import sniff, Ether, IP, TCP, UDP

protocols = {6: "TCP", 17: "UDP", 1: "ICMP"}

def packet_processing(packet):
    print("*" * 50)

    if packet.haslayer(Ether):
        ethernet = packet[Ether]
        print(f"[Ethernet] {ethernet.src} -> {ethernet.dst}")

    if packet.haslayer(IP):
        ip = packet[IP]
        print(f"[IP] {ip.src} -> {ip.dst} ({protocols.get(ip.proto, 'Other')})")

    if packet.haslayer(TCP):
        tcp = packet[TCP]
        print(f"[TCP] Src Port: {tcp.sport} -> Dst Port: {tcp.dport}")
    elif packet.haslayer(UDP):
        udp = packet[UDP]
        print(f"[UDP] Src Port: {udp.sport} -> Dst Port: {udp.dport}")

    
def main():

    duration = int(input("Enter sniffing time in seconds: "))
    choice = input("Filter only TCP packets? (Yes/No): ").strip().lower()

    print("[*] Starting the packet sniffer...")

    if choice == "yes":
        sniff(prn=packet_processing, store=False, timeout=duration, filter="tcp")
    else:
        sniff(prn=packet_processing, store=False, timeout=duration)
    
    
if __name__ == "__main__":
    main()