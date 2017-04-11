import socket
import json

host = '127.0.0.1'
port = 8000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(10)
quitting = False
print("Server Started.")

client, addr = s.accept()
while not quitting:
    try:
        data = json.loads(client.recv(3072).decode())
        if "<exit>" in data['message']:
            quitting = True
        if data['name'] not in clients:
            clients.append(data['name'])
            print("Added new client: ", data['name'])
            s.send(("Server: Welcome to chat, " + data['name']).encode())
        if data['message'] != '' and data['message'] != "<exit>":
            print("Client <{}> send to all: {} ".format(data['name'], data['message']))
    except:
        pass
s.close()
