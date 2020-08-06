#!/usr/local/bin/python3

import subprocess
import optparse

########################################################################
# User Defined Function/s
########################################################################

def change_mac(interface,new_mac):
    
    """This function will change the mac address"""
    # Putting interface down
    print(f"[+] Interface is set to {interface}")
    print(f"[+] New MAC is set to {new_mac}")
    print("[+] Putting interface down")
    subprocess.call(["ifconfig",interface,"down"])
    print("Interface down")
    # Changing the mac address
    print(f"[+] Changing the mac address to {new_mac}")
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    print("Mac address changed successfully")
    # Putting interface up
    print("[+] Putting interface up")
    subprocess.call(["ifconfig",interface,"up"])
    print("Interface is up")
    # Congratulations
    print("MAC address succesfully changed :)")

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface of which mac address you wanna change")
    parser.add_option("-m","--mac",dest="new_mac",help="The new MAC address that you want")
    (options,arguments) = parser.parse_args()
    return options.interface,options.new_mac

########################################################################
# Getting required values (Just by provided arguments)
########################################################################



########################################################################
# Getting required values (During program)
########################################################################

"""
interface = input("Enter the interface name or leave empty for wlan0 : ")
if not interface:
    interface = "wlan0"
print(f"[+] Interface is set to {interface}")

new_mac = input("Enter the new mac or leave empty for random : ")
if not new_mac:
    new_mac = "22:11:22:33:44:55"
"""

########################################################################
# Calling the function
########################################################################

(interface,new_mac) = get_arguments()
change_mac(interface,new_mac)
