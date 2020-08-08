#!/usr/local/bin/python

import subprocess
import optparse

########################################################################
# User Defined Function/s
########################################################################

def change_mac(interface,new_mac):
    
    """This function will change the mac address"""
    
    # Pre Image
    print() # Just a line break
    print(f"[>] Interface is set to {interface}")
    print(f"[>] New MAC is set to {new_mac}")
    
    # Putting interface down
    print() # Just a line break
    print("[+] Putting interface down")
    subprocess.call(["ifconfig",interface,"down"])
    
    # Changing the mac address
    print(f"[+] Changing the mac address of {interface} to {new_mac}")
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    
    # Putting interface up
    print("[+] Putting interface up")
    subprocess.call(["ifconfig",interface,"up"])

    # Addressing the user
    print() # Just a line break
    print("[>] We have done our best, if not successful, check the arguments you provided")

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface of which mac address you wanna change")
    parser.add_option("-m","--mac",dest="new_mac",help="The new MAC address that you want")
    (options,arguments) = parser.parse_args()
    return options.interface,options.new_mac


########################################################################
# Calling the function
########################################################################

(interface,new_mac) = get_arguments()

# Error Checking
if not interface or not new_mac:
    print("------------------------------------------------------------")
    print("Next time use command line arguments boy, You can do it\nType 'python3 mac_changer.py -h' for instructions")
    print("------------------------------------------------------------")
    if not interface:
        interface = input("Enter the interface you want to change : ")
    if not new_mac:
        new_mac = input("Enter the new mac : ")
    
change_mac(interface,new_mac)