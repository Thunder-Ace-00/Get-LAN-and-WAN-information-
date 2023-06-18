import subprocess
import re
import urllib.request
import socket

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

def get_nic_info():
    result = subprocess.run(["ip", "address"], capture_output=True, text=True)
    if result.returncode != 0:
        return None

    info = {}
    current_nic = None
    for line in result.stdout.splitlines():
        parts = line.split()
        if not line[0].isspace():  # New NIC section
            current_nic = parts[1].strip(":")
            info[current_nic] = {"ip4": None, "ip6": None, "mac": None}
        if parts[0] == "inet":
            info[current_nic]["ip4"] = parts[1].split("/")[0]
        elif parts[0] == "inet6":
            info[current_nic]["ip6"] = parts[1].split("/")[0]
        elif parts[0] == "link/ether":
            info[current_nic]["mac"] = parts[1]
    return info

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

def get_system_info():
    Is_Connected_Internet: bool = False
    Get_Wan_IP_Address: str     = "None"
    Get_Organization: str       = "None"
    Get_Country: str            = "None"

    try:
        urllib.request.urlopen('https://www.google.com', timeout=1)
        Is_Connected_Internet = True
    except urllib.error.URLError:
        pass

    Get_System_Name    = socket.gethostname()
    Get_Lan_IP_Address = get_nic_info()

    if Is_Connected_Internet:
        Get_Wan_IP_Address, Get_Organization, Get_Country = get_wan_info()

    return Get_System_Name, Get_Lan_IP_Address, Get_Wan_IP_Address, Get_Organization, Get_Country, Is_Connected_Internet

Pin_System_Name, Pin_Lan_IP, Pin_Wan_IP, Pin_Organization, Pin_Country, Pin_Connected = get_system_info()

# Use the values as needed
print(" -----------------------------------------------")
print(" Connected to Internet :", Pin_Connected)
print(" System Name           :", Pin_System_Name)

if isinstance(Pin_Lan_IP, dict):
    for nic, info in Pin_Lan_IP.items():
        print(" -----------------------------------------------")
        print(f" Info for {nic} :")
        print(" -----------------------------------------------")
        print(f" IPv4 Address          : {info['ip4']}")
        print(f" IPv6 Address          : {info['ip6']}")
        print(f" MAC Address           : {info['mac']}")
else:
    print(" -----------------------------------------------")
    print("LAN IP Address        :", Pin_Lan_IP)

print(" -----------------------------------------------")
print(" Info for WAN connection :")
print(" -----------------------------------------------")
print(" IP Address            :", Pin_Wan_IP)
print(" Organization          :", Pin_Organization)
print(" Country               :", Pin_Country)
print(" -----------------------------------------------")
