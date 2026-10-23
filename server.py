import socket
import threading
import logging

# Configuración básica del sistema de logs para imprimir eventos con marca de tiempo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ThreadedSocketServer:
    """
    Servidor TCP multihilo configurado para entorno LAN (0.0.0.0).
    Integra la difusión (broadcast), la identificación de usuarios y la trazabilidad en consola.
    """
    def __init__(self, host: str, port: int):
        self._host = host  # '0.0.0.0' (Todas las interfaces de red disponibles en la LAN)
        self._port = port
        
        # Diccionario dinámico para almacenar conexiones activas y sus nombres de usuario: {client_socket: username}
        self._clients = {}
        self._lock = threading.Lock()
        
        # Creación del socket principal del servidor
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _broadcast(self, message: str, sender_socket: socket.socket = None):
        """Difunde el mensaje de texto a todos los clientes conectados."""
        with self._lock:
            for client_socket in self._clients:
                if client_socket != sender_socket:
                    try:
                        client_socket.sendall(message.encode('utf-8'))
                    except Exception as e:
                        logging.error(f"Error al enviar mensaje a un cliente: {e}")

    def _handle_client(self, client_socket: socket.socket, address: tuple):
        """
        Gestiona la identificación inicial del usuario, la recepción de mensajes,
        el formateo con alias y el registro en consola de conexiones/desconexiones con IP y puerto.
        """
        ip, port = address
        username = "Anónimo"

        try:
            # 1. Identificación de Usuarios: El primer mensaje recibido del cliente es su alias
            raw_username = client_socket.recv(1024)
            if not raw_username:
                client_socket.close()
                return
            
            username = raw_username.decode('utf-8').strip()

            with self._lock:
                self._clients[client_socket] = username

            # 2. Registro detallado en consola indicando IP y Puerto de conexión
            logging.info(f"[CONEXIÓN] Cliente conectado desde IP: {ip}, Puerto: {port} con el usuario '{username}'")

            # Anunciar a los demás integrantes que un usuario se unió
            join_message = f"*** {username} se ha unido al chat ***\n"
            self._broadcast(join_message)

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                if message:
                    # Formatear el mensaje para mostrar quién lo envió (ej: [Juan]: Hola)
                    formatted_message = f"[{username}]: {message}\n"
                    logging.info(f"Mensaje de {username} ({ip}:{port}): {message}")
                    
                    # Reenviar el mensaje formateado a la sala
                    self._broadcast(formatted_message, client_socket)

        except Exception as e:
            logging.error(f"Error en la conexión con {username} ({ip}:{port}): {e}")
        finally:
            # 2. Registro detallado en consola de la desconexión indicando IP y Puerto
            with self._lock:
                if client_socket in self._clients:
                    del self._clients[client_socket]
            
            client_socket.close()
            logging.info(f"[DESCONEXIÓN] Cliente {username} ({ip}:{port}) se ha desconectado.")

            # Anunciar la salida del usuario a la sala
            leave_message = f"*** {username} ha salido del chat ***\n"
            self._broadcast(leave_message)

    def start(self) -> None:
        """Inicia el servidor y se queda escuchando de forma concurrente."""
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen()
        logging.info(f"Servidor iniciado y escuchando en {self._host}:{self._port} (Modo LAN)")

        try:
            while True:
                client_socket, address = self._server_socket.accept()
                
                # Crear un hilo independiente para atender a cada cliente de forma concurrente
                thread = threading.Thread(target=self._handle_client, args=(client_socket, address), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            logging.info("Servidor detenido por el usuario.")
        finally:
            self._server_socket.close()

if __name__ == "__main__":
    # Configuración obligatoria para red local (LAN)
    HOST = '0.0.0.0'
    PORT = 5000
    
    server = ThreadedSocketServer(HOST, PORT)
    server.start()
