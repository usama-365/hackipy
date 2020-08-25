#!/usr/bin/python

try:
    print("[>] Importing required modules")
    import scapy.all as scapy
    import argparse
    import subprocess
    import re
except ModuleNotFoundError:
    print("[!] Missing modules, Exiting...")
    exit()
else:
    print("[>] Modules Successfully imported")
    print() # Just a line break

########################################################################
# User Defined Functions
########################################################################

def arp_scan(ip):

    """This function will craft ARP packets and then broadcast them on the network
       It will then return a list of dictionaries consisting of filtered responses"""

    # Crafting the ARP packet
    print("[+] Crafting the ARP Packet/s to broadcast") if verbose else print(end="")
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = scapy.ARP(pdst=ip)
    arp_broadcast_packet = broadcast_packet / arp_packet
    
    # Sending the packet on the network and recieving the response
    print("[+] Sending the packet and recieving the responses in maximum 5 seconds") if verbose else print(end="")
    answered_packets_list = scapy.srp(arp_broadcast_packet,timeout=5,verbose=False)[0]
    
    # Filtering desired parts of responses and appending them into a list
    print("[+] Parsing the Responses") if verbose else print(end="")
    filtered_responses = []
    for answer in answered_packets_list:
        response = answer[1] # [0] of answer contains our request and [1] contains the response
        filtered_response = {
            "IP" : response.psrc,
            "MAC" : response.hwsrc,
        }
        filtered_responses.append(filtered_response)
    
    # Returning the filtered responses
    return filtered_responses


def show_result(responses):

    """This function will show the result of scan on screen"""

    print("[+] Displaying the responses in tabular form") if verbose else print(end="")
    print() if verbose else print()
    # Header
    print("      IP  \t|      MAC Address   ")
    print("-------------------------------------")
    # Content
    for response in responses:
        print(f" {response['IP']}\t| {response['MAC']}")

def get_arguments():

    """This function will get arguments from command line if there are any and return them to main function"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="ip",help="IP or IP range to scan, all if not provided")
    parser.add_argument("-v","--verbose",dest="vrb",help="Be Verbose? (0 for not, 1 for yes), 1 by default")
    options = parser.parse_args()
    return options.ip,options.vrb

def get_ip_range():

    """This function will craft the local IPv4 range string"""

    ip = str(subprocess.check_output(["hostname","-I"]))
    ip_range = re.search("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.",ip)
    ip_range = str(ip_range[0])
    ip_range += '1/24'
    return ip_range

########################################################################
# The main function
########################################################################

ip, verbose = get_arguments()

# Checking the arguments
verbose = False if verbose == '0' else True
ip = 'a' if not ip else ip

# Getting IP range if IP was not provided
if ip == 'a' or ip == 'A':
    ip = get_ip_range()

# Feedback
print(f"[>] IP (or IP Range) is set to {ip}")
print(f"[>] Verbose mode is set to {'ON' if verbose else 'OFF'}")

# Starting the scan
print() if verbose else print(end="")
print(f"[*] Starting the process") if verbose else print(end="")
print() if verbose else print(end="")
result = arp_scan(ip)

# Displaying the result
print() if verbose else print(end="")
show_result(result)