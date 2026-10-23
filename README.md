Sistema de Chat TCP Multihilo en Red Local (LAN)

Nota: Las diferentes versiones e implementaciones del proyecto estan distribuidas en diferentes ramas de este repositorio.

Aplicacion de chat desarrollada en Python basada en sockets TCP y concurrencia por hilos (threading), disenada para operar de manera optima en entornos de red local (LAN). El sistema implementa una arquitectura cliente-servidor concurrente que permite la comunicacion en tiempo real entre multiples usuarios de forma simultanea.

Caracteristicas Principales

* Arquitectura Cliente-Servidor Concurrente: Utiliza hilos independientes (threading) tanto en el servidor como en los clientes para garantizar la bidireccionalidad y evitar bloqueos durante el envio y recepcion de mensajes.
* Entorno LAN (0.0.0.0): El servidor esta configurado para escuchar en todas las interfaces de red disponibles, permitiendo la interconexion de diferentes equipos dentro de la misma red local.
* Sistema de Difusion (Broadcast): Propaga de forma automatica e inmediata los mensajes enviados por cualquier usuario hacia el resto de los participantes conectados en la sala.
* Identificacion de Usuarios: Solicita un alias o nombre de usuario unico al establecer la conexion para formatear y distinguir visualmente los mensajes en el chat (ej. [Usuario]: mensaje).
* Trazabilidad y Logs en Consola: El servidor registra y muestra detalladamente los eventos del sistema, indicando las direcciones IP y puertos de los clientes al conectarse o desconectarse.

Contribuciones y Equipo

Este proyecto es desarrollado colaborativamente, manteniendo un historial de versiones limpio y trazable que evidencia los aportes individuales de cada integrante del equipo mediante estrategias de control de versiones adaptadas a restricciones de red academica.
