from scapy.all import sniff, Ether, IP, TCP, UDP

protocol_map = { "TCP": 6, "UDP": 17, "ICMP": 1, "ALL": None}

protocols = {}

for k, v in protocol_map.items():   
    protocols[v] = k                  


def get_choice():

    while True:
        choice = input("Which protocol do you want to sniff? (TCP/UDP/ICMP/ALL): ")
        if choice in protocol_map:
            return choice
        else:
            print("Invalid choice.")

def get_file():

    while True:
        choice = input("Do you want to save the output to a file? (y/n): ").lower()
        if choice in ["y", "n"]:
            return choice == "y"
        else:
            print("Invalid input.")

def get_filter(protocol_choice):
    if protocol_choice == "ALL":
        return None
    else:
        return protocol_choice.lower()
    
def process_packet(packet, save=False, file=None):
    output = []

    if packet.haslayer(Ether):
        ethernet = packet[Ether]
        output.append(f"[Ethernet] {ethernet.src} -> {ethernet.dst}")

    if packet.haslayer(IP):
        ip = packet[IP]
        output.append(f"[IP] {ip.src} -> {ip.dst} (Protocol: {protocols.get(ip.proto, 'Other')})")

    if packet.haslayer(TCP):
        tcp = packet[TCP]
        output.append(f"[TCP] {tcp.sport} -> {tcp.dport}")
    elif packet.haslayer(UDP):
        udp = packet[UDP]
        output.append(f"[UDP] {udp.sport} -> {udp.dport}")

    result = "\n".join(output)
    print(result)
    print("*" * 50)

    if save and file:
        file.write(result + "\n" + "*" * 50 + "\n")

def main():

    protocol_choice = get_choice()
    bpf_filter = get_filter(protocol_choice)
    save_to_file = get_file()

    file = None
    if save_to_file == True:
        file = open("sniffed_packets.txt", "w")

    print(f"[*] Sniffing {protocol_choice} traffic... Press Ctrl+C to stop.\n")
    
    try:
        sniff(
            filter=bpf_filter,
            prn=lambda packet: process_packet(packet, save=save_to_file, file=file),
            store=False
        )
    except KeyboardInterrupt:
        print("[*] Stopped sniffing.")

    if file:
        file.close()
        print("[*] Output saved to sniffed_packets.txt")

if __name__ == "__main__":
    main()
    