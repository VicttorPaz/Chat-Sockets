Sistema de Chat Multihilo 

Nota: Las diferentes versiones e implementaciones del proyecto estan distribuidas en diferentes ramas de este repositorio.

Aplicacion de chat desarrollada en Python basada en sockets TCP y concurrencia por hilos (threading), disenada para operar de manera optima en entornos de red local (LAN). El sistema implementa una arquitectura cliente-servidor concurrente que permite la comunicacion en tiempo real entre multiples usuarios de forma simultanea.

Caracteristicas Principales

* Arquitectura Cliente-Servidor Concurrente: Utiliza hilos independientes (threading) tanto en el servidor como en los clientes para garantizar la bidireccionalidad y evitar bloqueos durante el envio y recepcion de mensajes.
* Entorno LAN (0.0.0.0): El servidor esta configurado para escuchar en todas las interfaces de red disponibles, permitiendo la interconexion de diferentes equipos dentro de la misma red local.
* Sistema de Difusion (Broadcast): Propaga de forma automatica e inmediata los mensajes enviados por cualquier usuario hacia el resto de los participantes conectados en la sala.
* Identificacion de Usuarios: Solicita un alias o nombre de usuario unico al establecer la conexion para formatear y distinguir visualmente los mensajes en el chat (ej. [Usuario]: mensaje).
* Trazabilidad y Logs en Consola: El servidor registra y muestra detalladamente los eventos del sistema, indicando las direcciones IP y puertos de los clientes al conectarse o desconectarse.

Instrucciones de Ejecucion Paso a Paso

1. Iniciar el servidor:
* Asegurese de tener Python instalado en el equipo que funcionara como servidor.
* Ejecute el script del servidor desde la terminal:
python servidor.py
* El servidor se iniciara escuchando en el puerto configurado sobre la red local (0.0.0.0).


2. Conectar los clientes:
* Desde otra terminal o equipo conectado a la misma red LAN, ejecute el script del cliente:
python cliente.py
* Introduzca la direccion IP local del servidor y el puerto correspondiente.
* Ingrese su alias o nombre de usuario cuando el sistema se lo solicite para unirse a la conversacion.



Como se Aplicaron los Principios SOLID y la Concurrencia

* Concurrencia: Se implemento la libreria threading en el servidor para atender de forma simultanea a multiples clientes mediante hilos independientes, evitando bloqueos en el ciclo principal de escucha. Asimismo, los clientes utilizan concurrencia para enviar y recibir mensajes de manera bidireccional y en tiempo real.
* Principios SOLID:
* Responsabilidad Unica (SRP): Cada componente del sistema tiene una funcion especifica y acotada, separando la logica de red de la gestion de eventos y la identificacion.
* Abierto/Cerrado (OCP): La arquitectura permite extender las funcionalidades de negocio o los manejadores de mensajes sin alterar la estructura central del servidor.
* Inversion de Dependencias (DIP): Los modulos de comunicacion operan desacoplados mediante inyeccion de dependencias y estructuras modulares.


Contribuciones y Equipo

Este proyecto es desarrollado colaborativamente, manteniendo un historial de versiones limpio y trazable que evidencia los aportes individuales de cada integrante del equipo mediante estrategias de control de versiones adaptadas a restricciones de red academica.
