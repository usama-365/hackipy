import subprocess
from random import choice as ch
import re
import scapy.all as scapy

################################################################################
# Global
################################################################################


def is_root():
    """This function will check whether the script was run as root or not"""

    current_user_id = int(subprocess.check_output(["id", "-u"]))
    if current_user_id == 0:
        return True
    else:
        return False


def nothing():
    """This function will do nothing"""

    pass

################################################################################
# Mac Modifier
################################################################################


def mac_is_valid(mac_address):
    """This function will check whether the mac is valid or not by structure"""

    try:
        # Check whether the colons are properly oriented
        for i in range(2, 15, 3):
            if not mac_address[i] == ":":
                return False
        # Check if first two digits are even
        if (int(mac_address[0:2]) % 2 == 0):
            return True
        return False
    except IndexError:
        return False


def generate_random_mac():
    """This function will generate and return a random mac address"""

    evens = [0, 2, 4, 6, 8]
    hexes = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F'
    ]
    random_mac = f"{ch(evens)}{ch(evens)}:{ch(hexes)}{ch(hexes)}:{ch(hexes)}{ch(hexes)}:{ch(hexes)}{ch(hexes)}:{ch(hexes)}{ch(hexes)}:{ch(hexes)}{ch(hexes)}"
    return random_mac


def get_default_interface():
    """This function will return the default network interface"""

    default_routing_table = (str(subprocess.check_output("route")))[0:-3]
    default_interface = re.search('\s+\S*$', default_routing_table)
    default_interface = default_interface[0][1:]

    return default_interface


def get_current_mac(interface):
    """This function will return the current MAC of the provided interface"""

    # Get the current mac of interface
    try:
        ifconfig_output = str(subprocess.check_output(["ifconfig", interface]))
        mac_address = re.search(
            "\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)
    # If the interface is not valid
    except:
        print("[!] Please enter a valid interface")
        exit()
    return mac_address[0]


def change_mac(new_mac, interface, mute):
    """This function will change the mac address"""

    print() if not mute else nothing()
    print("[+] Putting interface down") if not mute else nothing()
    subprocess.call(["ifconfig", interface, "down"])
    print("[+] Changing MAC") if not mute else nothing()
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    print("[+] Putting interface up") if not mute else nothing()
    subprocess.call(["ifconfig", interface, "up"])

################################################################################
# Network Scanner
################################################################################


def get_ip_range():
    """This function will craft the local IPv4 whole range string"""

    ip = str(subprocess.check_output(["hostname", "-I"]))
    ip_range = re.search("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.", ip)
    ip_range = str(ip_range[0])
    ip_range += '1/24'
    return ip_range


def arp_scan(ip, mute):
    """This function will craft ARP packets and then broadcast them on the network.
       It will then return a list of dictionaries {"IP":ip, "MAC":mac} of response"""

    # Crafting the ARP packet
    print("[+] Crafting the ARP Packet/s to broadcast") if not mute else nothing()
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_arp_packet = broadcast_packet / arp_packet

    # Sending the packet on the network and recieving the response (3 times)
    print("[+] Sending the packet and recieving the responses in maximum 10 seconds")
    answered_packets_list = scapy.srp(
        broadcast_arp_packet, timeout=3, verbose=False)[0]
    answered_packets_list.extend(scapy.srp(
        broadcast_arp_packet, timeout=3, verbose=False)[0])
    answered_packets_list.extend(scapy.srp(
        broadcast_arp_packet, timeout=3, verbose=False)[0])

    # Filtering desired parts of responses and appending them into a list
    print("[+] Parsing the Responses") if not mute else nothing()
    filtered_responses = parse_responses(answered_packets_list)

    # Returning the filtered responses
    return filtered_responses


def parse_responses(answered_packets_list):
    """This function will filter the response of answered packets list 
       and structure it into a dictionary"""

    filtered_responses = []
    for answer in answered_packets_list:
        # [0] of answer contains our request and [1] contains the response in answered packet
        response = answer[1]
        filtered_response = {
            "IP": response.psrc,
            "MAC": response.hwsrc,
        }
        # Check if it is already in the list or not
        if filtered_response in filtered_responses:
            nothing()
        else:
            filtered_responses.append(filtered_response)

    return filtered_responses


def show_result(parsed_responses, mute):
    """This function will display the parsed response in tabular form"""

    print("[+] Displaying the responses in tabular form") if not mute else nothing()
    print()
    # Header
    print("      IP  \t|      MAC Address   ")
    print("-------------------------------------")
    # Content
    for response in parsed_responses:
        print(f" {response['IP']}\t| {response['MAC']}")
