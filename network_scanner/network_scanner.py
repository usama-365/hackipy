#!/usr/bin/python

import scapy.all as scapy

def scan(ip):
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = scapy.ARP(pdst=ip)
    arp_broadcast_packet = broadcast_packet / arp_packet
    answered_list = scapy.srp(arp_broadcast_packet,timeout=5,verbose=False)[0]
    # Header
    print("      IP  \t|      MAC Address   ")
    for answer in answered_list:
        response = answer[1]
        print("----------------------------------------")
        print(f" {response.psrc}\t|   {response.hwsrc}")
        

scan("192.168.10.1/24")