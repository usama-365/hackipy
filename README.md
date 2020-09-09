# hackipy
## About the repository
Hacking, pentesting and cyber-security related tools/scripts built with Python (3 of course). I have created these tools for my personal use but I am also publishing them here because I am not a closed-source giant. If these tools will help you or make your workflow easier, I'll be happy.

## Installation
**This guide is written keeping new-bies in mind, if you are a seasoned professional, simply clone the repository***
Go to home directory
'''bash
cd
'''
Clone the repository
'''bash
git clone https://github.com/usama-365/pyhack
'''
Change to the cloned repository/directory
'''bash
cd pyhack
'''
To run any tool, simply
'''bash
./tool_name.py
'''
## About the tools
**Note** : All tools are optimized to work without arguments (So you don't get afraid of errors without specifying them). Simply put, the arguments are optional. But it is still recommended to use arguments as they make the workflow faster and efficient.
#### mac_modifier.py
It is as it sounds. Another mac changer in the market. Changes the mac address of the provided interface (default if not provided) to the provided mac (random if not provided).
'''
./mac_modifier.py [arguments]
'''
Arguments :
> -i,--interface : Specify the interface of which MAC you want to change (If not provided, default interface would be selected)

> -m,--mac       : Specify the new MAC address (A random MAC address will be calculated if not provided)

> -s,--silent    : Show less output (Not recommended if you want to look cool)

> -h,--help      : Show help (Somewhat similar to this)
