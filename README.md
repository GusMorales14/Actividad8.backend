# Actividad8.backend
Actividad 8. Backend Análisis, diseño y construcción de software 

Link a video demostrativo: https://youtu.be/noVzjxLXHq8

El archivo crud_service.py es la aplicación principal desarrollada con Flask; en ella definí los servicios web CRUD que se conectan a la base de datos MySQL que corre dentro del contenedor Docker.

El archivo datos_iniciales.py se utiliza para insertar datos de ejemplo en la tabla vehicle_snap, de manera que ya existan registros cuando pruebo los servicios.

Finalmente, el archivo consumir_vehicle_snap.py es el programa cliente que consume los servicios web mediante peticiones GET, POST, PUT y DELETE
