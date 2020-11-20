#!/usr/bin/python3

try:
    print("[>] Importing required modules")
    from utilities import is_root, nothing, get_ip_range, arp_scan, parse_responses, show_result
    import argparse
except ModuleNotFoundError:
    print("[!] Missing modules, Exiting...")
    exit()
else:
    print("[>] Modules Successfully imported")
    print()  # Just a line break

########################################################################
# User Defined Function
########################################################################


def get_arguments():
    """This function will get arguments from command line if there are any and return them to main function"""

    parser = argparse.ArgumentParser(description="All arguments are optional")
    parser.add_argument("-t", "--target", dest="ip",
                        help="IP or IP range to scan, all if not provided")
    parser.add_argument("-s", "--silent", dest="mute",
                        help="Show less output", action="store_true")
    options = parser.parse_args()
    return options.ip, options.mute

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
    try:
        ip = get_ip_range()
    except TypeError:
        print("[!] Can't get current network's IP range, Not connected to a network")
        exit()
print(f"[>] IP (or IP Range) is set to {ip}") if not mute else nothing()

# Starting the scan
print() if not mute else nothing()
print(f"[+] Starting the scan") if not mute else nothing()
print() if not mute else nothing()
responses = arp_scan(ip, mute)

# Displaying the responses
print() if not mute else nothing()
if (responses):
    show_result(responses, mute)
else:
    print("[!] No response recieved!")
