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

def nothing():

    """Nothing ;)"""

    pass

def is_root():
    
    """This function will check whether the script was run as root or not"""

    current_user_id = int(subprocess.check_output(["id","-u"]))
    if current_user_id == 0:
        return True
    else:
        return False

def get_arguments():

    """This function will get arguments from command line if there are any and return them to main function"""

    parser = argparse.ArgumentParser(description="All arguments are optional")
    parser.add_argument("-t","--target",dest="ip",help="IP or IP range to scan, all if not provided")
    parser.add_argument("-s","--silent",dest="mute",help="Show less output",action="store_true")
    options = parser.parse_args()
    return options.ip,options.mute

def get_ip_range():

    """This function will craft the local IPv4 range string"""

    ip = str(subprocess.check_output(["hostname","-I"]))
    ip_range = re.search("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.",ip)
    ip_range = str(ip_range[0])
    ip_range += '1/24'
    return ip_range

def arp_scan(ip):

    """This function will craft ARP packets and then broadcast them on the network
       It will then return a list of dictionaries consisting of filtered responses"""

    # Crafting the ARP packet
    print("[+] Crafting the ARP Packet/s to broadcast") if not mute else nothing()
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = scapy.ARP(pdst=ip)
    arp_broadcast_packet = broadcast_packet / arp_packet
    
    # Sending the packet on the network and recieving the response
    print("[+] Sending the packet and recieving the responses in maximum 5 seconds")
    answered_packets_list = scapy.srp(arp_broadcast_packet,timeout=5,verbose=False)[0]
    
    # Filtering desired parts of responses and appending them into a list
    print("[+] Parsing the Responses") if not mute else nothing()
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

    print("[+] Displaying the responses in tabular form") if not mute else nothing()
    print()
    # Header
    print("      IP  \t|      MAC Address   ")
    print("-------------------------------------")
    # Content
    for response in responses:
        print(f" {response['IP']}\t| {response['MAC']}")

########################################################################
# The main function
########################################################################

# Parsing the arguments
ip, mute = get_arguments()

# Checking for privileges
if is_root():
    nothing()
else:
    print("[!] Please run the script as root")
    exit()

# Getting local IP range if IP is not provided and providing feedback
if not ip:
    ip = get_ip_range()
print(f"[>] IP (or IP Range) is set to {ip}") if not mute else nothing()

# Starting the scan
print() if not mute else nothing()
print(f"[+] Starting the scan") if not mute else nothing()
print() if not mute else nothing()
result = arp_scan(ip)

# Displaying the result
print() if not mute else nothing()
show_result(result)