import socket
import json


shutdown = False

host = '127.0.0.1'
port = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

name = input("Name: ")
j = json.dumps({"name": name, "message": ""})
s.sendall(j.encode())

while not shutdown:
    message = input(name + "-> ")
    if message != "":
            jsn = json.dumps({"name": name, "message": message})
            s.send(jsn.encode())


shutdown = True
s.close()
