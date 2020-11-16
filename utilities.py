import subprocess
from random import choice as ch
import re


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
