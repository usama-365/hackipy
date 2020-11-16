#!/usr/bin/python3

try:
    print("[>] Importing required modules")
    from utilities import is_root, nothing, mac_is_valid, change_mac, generate_random_mac, get_current_mac, get_default_interface
    import argparse
except ModuleNotFoundError:
    print("[!] Missing modules, Exiting...")
    exit()
else:
    print("[>] Modules successfully imported")
    print()  # Just a line break

########################################################################
# User Defined Functions
########################################################################


def get_arguments():
    """This function will capture arguments from the command line if there are any and return them"""

    parser = argparse.ArgumentParser(description="All arguments are optional")
    parser.add_argument("-i", "--interface", dest="interface",
                        help="Interface of which mac address you wanna change")
    parser.add_argument("-m", "--mac", dest="new_mac",
                        help="The new MAC address that you want")
    parser.add_argument("-s", "--silent", dest="mute",
                        help="Show less output", action="store_true")
    options = parser.parse_args()
    return options.interface, options.new_mac, options.mute


########################################################################
# The main function
########################################################################

# Parsing the arguments
interface, new_mac, mute = get_arguments()

# Checking for privileges
if is_root():
    nothing()
else:
    print("[!] Script must be run as root")
    exit()

# If the arguments are not provided, notify
if not interface:
    print("[-] Interface not provided, selecting the default") if not mute else nothing()
    interface = get_default_interface()
if not new_mac:
    print("[-] Custom MAC not provided, generating a random MAC") if not mute else nothing()
    new_mac = generate_random_mac()

print() if not mute else nothing()  # Just a line break

# Getting the current MAC
mac_address_before_changing = get_current_mac(interface)

# Checking whether the new MAC is valid or not and performing operations accordingly
if mac_is_valid(new_mac):
    print(
        f"[>] Current MAC address is {mac_address_before_changing}") if not mute else nothing()
    print(f"[>] Interface is set to {interface}") if not mute else nothing()
    print(f"[>] New MAC is set to {new_mac}") if not mute else nothing()
    # Changing the MAC
    change_mac(new_mac, interface, mute)
else:
    print("[!] Your provided MAC address is not valid, It should be in form of XX:XX:XX:XX:XX:XX and first two digits should be even")
    exit()

print() if not mute else nothing()  # Just a line break

# Checking whether the MAC address has changed or not
if mac_address_before_changing != get_current_mac(interface):
    print("[+] MAC address changed successfully ;)")
else:
    print("[-] MAC address is not changed due to some reason :(")
