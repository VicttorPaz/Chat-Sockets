import socket
import threading
import logging

# Configuración básica del sistema de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ThreadedSocketServer:
    """
    Servidor TCP multihilo configurado para entorno LAN (0.0.0.0).
    Encargado de abrir el puerto, aceptar conexiones y gestionar la difusión (broadcast).
    """
    def __init__(self, host: str, port: int):
        self._host = host  # '0.0.0.0' (Todas las interfaces de red disponibles en la LAN)
        self._port = port
        
        # Registro dinámico de clientes conectados y control de concurrencia
        self._clients = []
        self._lock = threading.Lock()
        
        # Creación del socket principal del servidor
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _broadcast(self, message: bytes, sender_socket: socket.socket):
        """Difunde el mensaje recibido a todos los clientes conectados excepto al emisor."""
        with self._lock:
            for client in self._clients:
                if client != sender_socket:
                    try:
                        client.sendall(message)
                    except Exception as e:
                        logging.error(f"Error al enviar mensaje a un cliente: {e}")

    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """Gestiona la comunicación individual y el ciclo de vida del cliente conectado."""
        ip, port = address
        logging.info(f"[CONEXIÓN] Cliente conectado desde IP: {ip}, Puerto: {port}")
        
        with self._lock:
            self._clients.append(client_socket)

        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Reenviar el mensaje a los demás integrantes de la red
                self._broadcast(data, client_socket)
        except Exception as e:
            logging.error(f"Error en la conexión con {ip}:{port}: {e}")
        finally:
            with self._lock:
                if client_socket in self._clients:
                    self._clients.remove(client_socket)
            client_socket.close()
            logging.info(f"[DESCONEXIÓN] Cliente {ip}:{port} se ha desconectado.")

    def start(self) -> None:
        """Inicia el servidor y se queda escuchando de forma concurrente."""
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        logging.info(f"Servidor iniciado y escuchando en {self._host}:{self._port} (Modo LAN)")

        try:
            while True:
                client_socket, address = self._server_socket.accept()
                
                # Crear un hilo independiente para atender a cada cliente sin bloquear a los demás
                thread = threading.Thread(target=self._handle_client, args=(client_socket, address), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            logging.info("Servidor detenido por el usuario.")
        finally:
            self._server_socket.close()

if __name__ == "__main__":
    # Configuración obligatoria para red local (LAN)
    HOST = '0.0.0.0'
    PORT = 
    
    server = ThreadedSocketServer(HOST, PORT)
    server.start()
