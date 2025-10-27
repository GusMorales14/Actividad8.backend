import mysql.connector

# Configurar conexión a MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",       # Docker  MySQL en localhost
    user="root",
    password="contrasena", 
    database="trafico",
    port=3306
)

cursor = conn.cursor()

# Función para insertar un registro
def insert_vehicle_snapshot(car_count, truck_count, motorcycle_count, bus_count):
    total_count = car_count + truck_count + motorcycle_count + bus_count
    sql = """
        INSERT INTO vehicle_snap (car_count, truck_count, motorcycle_count, bus_count, total_count)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (car_count, truck_count, motorcycle_count, bus_count, total_count)
    cursor.execute(sql, values)
    conn.commit()
    print(f"Registro insertado correctamente: total={total_count}")

# Datos de prueba
data = [
    (12, 3, 5, 1),
    (10, 2, 4, 0),
    (5, 1, 2, 1),
    (8, 0, 3, 0)
]

# Insertar los registros
for record in data:
    insert_vehicle_snapshot(*record)

# Cerrar conexión
cursor.close()
conn.close()

print("Inserciones completadas con éxito.")
