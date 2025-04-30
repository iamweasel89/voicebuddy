import socket

def main():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Сервер слушает на {host}:{port}...")

    try:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Подключение от {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Получено: {data.decode()}")
                conn.sendall("Блок принят".encode('utf-8'))

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        server_socket.close()
        print("Сервер остановлен.")

if __name__ == "__main__":
    main()
