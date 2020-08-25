#!/usr/bin/python3

try:
    print("[>] Importing required modules")
    import subprocess
    import argparse
    import re
    from random import choice as ch
except ModuleNotFoundError:
    print("[!] Missing modules, Exiting...")
    exit()
else:
    print("[>] Modules successfully imported")
    print() # Just a line break

########################################################################
# User Defined Functions
########################################################################

def get_arguments():

    """This function will capture arguments from the command line if there are any and return them"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help="Interface of which mac address you wanna change")
    parser.add_argument("-m","--mac",dest="new_mac",help="The new MAC address that you want")
    options = parser.parse_args()
    return options.interface,options.new_mac

def mac_is_valid(mac_to_check):
    
    """This function will return a boolean value based on wheter the MAC address is correct or not"""

    # Validating the MAC address
    try:
        # Checking whether the format is correct
        if mac_to_check[2] == ":" and mac_to_check[5] == ":" and mac_to_check[8] == ":" and mac_to_check[11] == ":" and mac_to_check[14] == ":":
            # Checking whether the first two digits are even
            if (int(mac_to_check[0:1]) % 2) == 0:
                return True
            else:
                return False
        else:
            return False
    # If no. of digits are incomplete
    except IndexError:
        return False

def generate_random_mac():

    """This function will generate a random MAC address"""

    evens = [0,2,4,6,8]
    hexes = [
        0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F'
    ]
    randomly_generated_mac = f"{ch(evens)}{ch(evens)}:{ch(hexes)}{ch(hexes)}:{ch(hexes)}{ch(hexes)}:{ch(hexes)}{ch(hexes)}:{ch(hexes)}{ch(hexes)}:{ch(hexes)}{ch(hexes)}"
    return randomly_generated_mac

def get_default_interface():

    """This function will return default interface"""

    default_routing_table = str(subprocess.check_output(["route","|","grep","default"],shell=True))
    default_interface = re.search("[lawethn]{3,4}[\d]{1,2}",default_routing_table)
    
    return default_interface[0]

def get_current_mac(interface):
    
    """This function will return the current MAC of the provided interface"""
    
    # Get the current mac of interface
    try:
        ifconfig_output = str(subprocess.check_output(["ifconfig",interface]))
        mac_address = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_output)
    # If the interface is not valid
    except:
        print("[!] Please enter a valid interface")
        exit()
    return mac_address[0]

def change_mac(interface,new_mac):
    
    """This function will change the mac address"""
    
    print() # Just a line break

    # Putting interface down
    print("[+] Putting interface down")
    subprocess.call(["ifconfig",interface,"down"])
    
    # Changing the mac address
    print(f"[+] Changing the mac address of {interface} to {new_mac}")
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    
    # Putting interface up
    print("[+] Putting interface up")
    subprocess.call(["ifconfig",interface,"up"])

########################################################################
# The main function
########################################################################

(interface,new_mac) = get_arguments()

# If the arguments are not provided, manually input them

if not interface:
    print("[-] Interface not provided, selecting the default")
    interface = get_default_interface()
if not new_mac:
    print("[-] Custom MAC not provided, generating a random MAC")
    new_mac = generate_random_mac()

print() # Just a line break

# Getting the current MAC
mac_address_before_changing = get_current_mac(interface)

#Checking whether the new MAC is valid or not and performing operations accordingly
if mac_is_valid(new_mac):
    print(f"[>] Current MAC address is {mac_address_before_changing}")
    print(f"[>] Interface is set to {interface}")
    print(f"[>] New MAC is set to {new_mac}")
    # Changing the MAC
    change_mac(interface,new_mac)
else:
    print("[!] Your provided MAC address is not valid, It should be in form of XX:XX:XX:XX:XX:XX and first two digits should be even")
    exit()

print() # Just a line break

# Checking whether the MAC address has changed or not
if mac_address_before_changing != get_current_mac(interface):
    print("[+] MAC address changed successfully ;)")
else:
    print("[-] MAC address is not changed due to some reason :(\n[*] Make sure to run the script as root")