import socket
import threading
import sys
import logging

# Configuración básica del sistema de logs para imprimir mensajes formateados en la consola
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SocketClient:
    """
    Cliente de chat concurrente persistente. 
    Mantiene una conexión abierta con el servidor y utiliza hilos paralelos para 
    escribir mensajes por consola y recibir las transmisiones en tiempo real.
    """
    def __init__(self, host: str, port: int, alias: str):
        self._host = host
        self._port = port
        self._alias = alias
        self._buffer_size = 1024
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _receive_messages(self) -> None:
        """Hilo secundario dedicado exclusivamente a escuchar y mostrar los mensajes del servidor sin bloqueos."""
        while True:
            try:
                response = self._sock.recv(self._buffer_size)
                if not response:
                    print("\n[Desconectado]: El servidor ha cerrado la conexión.")
                    break
                print(response.decode('utf-8'), end='')
            except socket.error:
                print("\n[Error]: Se perdió la conexión con el servidor.")
                break

    def start(self) -> None:
        """Conecta al servidor, envía el alias, arranca el hilo de lectura y permite enviar mensajes libremente."""
        try:
            # 1. Establecemos conexión persistente con el servidor en la LAN
            self._sock.connect((self._host, self._port))
            
            # 2. Enviamos el alias de usuario como primer mensaje obligatorio
            self._sock.sendall(self._alias.encode('utf-8'))
            
            logging.info("Conectado exitosamente al chat. Escribe tus mensajes (o escribe '/salir' para terminar):")

            # 3. Lanzamos el hilo secundario en segundo plano para escuchar respuestas en tiempo real
            receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            receive_thread.start()

            # 4. Bucle principal interactivo para redactar y enviar mensajes en cualquier momento
            while True:
                message = input()
                if message.lower() == '/salir':
                    break
                if message.strip():
                    self._sock.sendall(message.encode('utf-8'))

        except socket.error as e:
            logging.error(f"Error de comunicación con el servidor: {e}")
        finally:
            self._sock.close()
            sys.exit(0)


# --- EJECUCIÓN PRINCIPAL DEL CLIENTE ---
if __name__ == "__main__":

    HOST = '172.17.39.2'
    PORT = 8888
    ALIAS = 'Sebas'  


    # Instanciamos nuestro objeto cliente pasándole las coordenadas del servidor y el alias
    client = SocketClient(HOST, PORT, ALIAS)
    client.start()