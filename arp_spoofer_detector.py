#!/usr/bin/python3

import scapy.all as scapy
import argparse

def get_arguments():

    """This function will get arguments from command line"""

    parser = argparse.ArgumentParser(description="All arguments are optional")
    parser.add_argument("-i","--interface",help="Interface to sniff on",dest="interface")
    parser.add_argument("-s","--silent",help="Show less output",action="store_true",dest='mute')
    options = parser.parse_args()
    return options.interface,options.mute

def get_mac(ip):

    """This function will get the MAC address of the argument (IP) by ARP request"""

    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast_packet = broadcast_packet / arp_packet
    answered = scapy.srp(arp_broadcast_packet,timeout=2,verbose=False)[0]
    try:
        return answered[0][1].hwsrc
    except IndexError:
        return None

def sniff(interface):

    """This function will sniff packets on provided interface
       and call process_packet function to filter and display
       the result"""

    print("[>] Sniffing started, Capturing interesting packets\n")
    scapy.sniff(iface=interface,store=False,prn=process_packet)

def process_packet(packet):
    """This function will process the packets being sniffed for analysis"""
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        real_mac_address = get_mac(packet[scapy.ARP].psrc)
        if real_mac_address:
            if real_mac_address != packet[scapy.ARP].hwsrc:
                print("[+] Warning! ARP spoofing detected")
            

interface, mute = get_arguments()
sniff(interface)