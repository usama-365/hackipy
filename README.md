# hackipy
## Disclaimer
**All the provided tools are for legal use only by white-hat hackers, cyber-security related people and pentesters, the author is not responsible for any misuse of these tools.**
## About the repository
hackipy is a collection of hacking, pentesting and cyber-security related tools/scripts built with Python (3 of course). I have created these tools for my personal use but I am also publishing them here because I am not a closed-source giant. If these tools will make your workflow easier or help you, I'll be happy. (I believe in get from the community, give to the community).

## Installation
**This guide is written keeping new-bies in mind, if you are a seasoned professional, simply clone the repository.**

Go to home directory
```bash
cd
```
Clone the repository
```bash
git clone https://github.com/usama-365/hackipy.git
```
Change to the cloned repository (which is now directory)
```bash
cd hackipy
```
To run any tool, simply type
```bash
./tool_name.py
```
## About the tools
**Note** : All tools are optimized to work without arguments (So you don't get afraid of errors when you not provide them). Simply, the arguments are optional for every tool. But it is still recommended to use arguments as they make the workflow faster and efficient.
#### 1) mac_modifier.py
It is as it sounds. Another mac changer in the market. Changes the mac address of the provided interface (selects default interface if not provided) to the provided mac (generates random mac if not provided). Usually used before any pentesting session for anonymity.
```bash
./mac_modifier.py [arguments]
```
Arguments :
> -i,--interface X : Specify the interface (X) of which MAC you want to change (If not provided, default interface would be selected)
>
> -m,--mac X       : Specify the new MAC address (X) (A random MAC address will be calculated if not provided)
>
> -s,--silent      : Show less output (Not recommended if you want to look cool)
>
> -h,--help        : Show help (Somewhat similar to this)

#### 2) network_scanner.py
Scans the network for client/s and show the output in formatted manner. Takes IP or IP range as argument and selects all the IP's of current network if IP or IP range not provided. Usually used after changing mac_address for anonymity.
```bash
./network_scanner.py [arguments]
```
Arguments :
> -t,--target X    : IP or IP range (X) to scan, all if not provided
>
> -s,--silent      : Show less output (Not recommended if you want to look cool)
>
> -h,--help        : Show help (Somewhat similar to this)

#### 3) arp_spoofer.py
Exploits the weakness of ARP protocol to redirect packet flow between two targets through your machine. Makes you MITM (man-in-the-middle). Takes IP address of two targets as argument (inputs manually if IP's are not provided at all or not provided correctly). Starts sending spoof packets to both. Restores the ARP table by sending honest responses when stopped to make things normal ASAP. Usually used after network_scanner.py on the discovered hosts.
```bash
./arp_spoofer.py [arguments]
```
Arguments :
> -t,--targets X Y : IP pair (X and Y) to spoof
>
> -s,--silent      : Show less output (Not recommended if you want to look cool)
>
> -h,--help        : Show help (Somewhat similar to this)

#### 4) packet_sniffer.py
Sniffs the packets on the provided interface (Selects default interface if not provided). Extracts **DNS requests** (Helps in sniffing some URL's victim is visiting), **URL's being visited** (in HTTP requests, includes URL's of sites, images, videos and other HTTP content) and **Usernames and Passowrds** (Transmitted through HTTP). Usually used after you become MITM by arp_spoofer.py to sniff packets that are being forwarded through your machine. It can also sniff packets of your machine that are being transferred through the selected network interface.
```bash
./packet_sniffer.py [arguments]
```
Arguments :
> -i,--interface X : Interface (X) to sniff on, default if not provided
>
> -s,--silent      : Show less output (Not recommended if you want to look cool)
>
> -h,--help        : Show help (Somewhat similar to this)

#### 5) dns_spoofer.py
Spoofs and manipulate the DNS responses to redirect the (victim) machine recieving the responses where you want. Takes the target DNS (meaning specific DNS responses you want to manipulate for custom redirection) and spoof IP (that can be IP of webserver/website which will be replaced in original DNS response to redirect the victim) as argument. Creates a queue where packets are stored and releases the packets after manipulation. Arguments can also be provided to spoof packets of your own machine (INPUT and OUTPUT chain) rather than the victim machine (FORWARD chain that includes victim packets flowing through your machine after you become MITM) and also to totally block the packets. Usually used after becoming MITM by arp_spoofer.py and in paralell with packet_sniffer.py to sniff the interesting packets after redirecting the victim to a not so secure webpage or website using DNS spoofing.
```bash
./dns_spoofer [arguments]
```
Arguments :
> -io,--inout        : Spoof the DNS packets of your machine rather than the victim machine (forwarded packets)
>
> -b,--block         : Block/Drop the packets entirely (No Internet)
>
> -td,--target-dns X : Target a specific DNS response (X) (e.g. www.example.com) for manipulating and spoofing, targets and spoofs every DNS response if not provided
>
> -si,--spoof-ip X	 : IP (X) that would take place of original IP in DNS response for custom redirection of victim, the victim will be redirected to this IP (X)
>
> -s,--silent        : Show less output (Not recommended if you want to look cool)
>
> -h,--help          : Show help (Somewhat similar to this)

#### 6) file_interceptor.py
Monitors for HTTP GET requests for files and intercepts the responses. Manipulates the response to serve the victim **dangerous** files rather than the ones he/she intended for. Whenever the victim will request for a file download over HTTP, the original download link will be replaced with the link you provide. Takes (direct) download link of the **dangrous** file as an argument (compulsory). Also takes the file type/extension to target for (For example .exe) as an argument (and if not provided, then automatically selects some common formats, for example .pdf, .exe, .doc etc, *More will be added soon*). Usually used after becoming MITM with arp_spoofer.py to replace the files the victim wants to download with backdoors, credential harvesters, keyloggers etc.
```bash
./file_interceptor.py [arguments]
```
Arguments :
> -r,--replace X       : Direct download link/URL (X) of the file you want to replace with original file
>
> -f,--filetype X      : File type (X) to target for (e.g. .exe) (Selects common filetypes if not provided)
>
> -io,--inout 	       : Intercept the file from your machine rather than the victim machine (forwarded packets)
>
> -d,--display	   	   : Display the intercepted packets content before and after manipulation (Just for in-depth analysis, can clutter your screen)
>
> -s,--silent          : Show less output (Not recommended if you want to look cool)
>
> -h,--help            : Show help (Somewhat similar to this)

**To be continued**
