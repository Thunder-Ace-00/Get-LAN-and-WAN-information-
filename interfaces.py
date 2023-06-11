import socket
import netifaces
import urllib.request
import urllib.error
import subprocess

'''
---------------------------------------------------------------------------------------
Copyright (c) 2023-2024 R.Bleeker

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
---------------------------------------------------------------------------------------
'''

def get_lan_ip():
    interfaces = netifaces.interfaces()
    ips = {}

    for interface in interfaces:
        if interface.startswith(('eth', 'wlan', 'enp', 'wlp', 'enx', 'wlx')):
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                ip_address = addresses[netifaces.AF_INET][0]['addr']
                ips[interface] = ip_address

    if not ips:
        return "No LAN interface(s) found !"

    return ', '.join(f'{k}: {v}' for k, v in ips.items())


def get_wan_info() -> tuple[str, str, str]:
    try:
        cmd               = """echo "External IP: $(curl -s ifconfig.me) --- Organization: $(whois $(curl -s ifconfig.me) | grep -i 'org-name' | awk '{for(i=2;i<=NF;++i) {if(i!=2) printf " "; printf "%s", $i}}') --- Country: $(whois $(curl -s ifconfig.me) | grep -i 'country' | awk '{print $2}' | head -n 1)" """
        output            = subprocess.check_output(cmd, shell=True)
        result            = output.decode('utf-8').strip()

        values            = result.split(' --- ')
        external_ip       = values[0].split(': ')[1]
        Read_Organization = values[1].split(': ')[1]
        Read_Country      = values[2].split(': ')[1]

        return external_ip, Read_Organization, Read_Country
    except subprocess.CalledProcessError:
        return "", "", ""


def get_system_info() -> tuple[str, str, str, str, str, bool]:
    Is_Connected_Internet: bool = False
    Get_Wan_IP_Address: str     = "No WAN interface(s) found !"
    Get_Organization: str       = "Not found !"
    Get_Country: str            = "Not found !"

    try:
        urllib.request.urlopen('https://www.google.com', timeout=1)
        Is_Connected_Internet = True
    except urllib.error.URLError:
        pass

    Get_System_Name    = socket.gethostname()
    Get_Lan_IP_Address = get_lan_ip()

    if Is_Connected_Internet:
        Get_Wan_IP_Address, Get_Organization, Get_Country = get_wan_info()

    return Get_System_Name, Get_Lan_IP_Address, Get_Wan_IP_Address, Get_Organization, Get_Country, Is_Connected_Internet


Pin_System_Name, Pin_Lan_IP, Pin_Wan_IP, Pin_Organization, Pin_Country, Pin_Connected = get_system_info()

# Use the values as needed
print("Connected to Internet :", Pin_Connected)
print("System Name           :", Pin_System_Name)
print("LAN IP Address        :", Pin_Lan_IP)
print("WAN IP Address        :", Pin_Wan_IP)
print("Organization          :", Pin_Organization)
print("Country               :", Pin_Country)
