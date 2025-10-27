from flask import Flask, request, jsonify
import mysql.connector

# Configuración de la conexión a MySQL
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "constrasena",   
    "database": "trafico",       # base de datos
    "port": 3306
}

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**db_config)

# ------------------ CRUD ------------------

# GET: obtener todos los registros
@app.route("/vehicle_snap", methods=["GET"])
def get_vehicle_snap():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicle_snap")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# GET: obtener un registro por id
@app.route("/vehicle_snap/<int:id_input>", methods=["GET"])
def get_vehicle_snap(id_input):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicle_snap WHERE id_input = %s", (id_input,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return jsonify(record)
    return jsonify({"error": "Registro no encontrado"}), 404

# POST: crear un nuevo registro
@app.route("/vehicle_snap", methods=["POST"])
def create_vehicle_snap():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vehicle_snap (class, count_value) VALUES (%s, %s)",
        (data["class"], data["count_value"])
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"id_input": new_id, "message": "Registro creado"}), 201

# PUT: actualizar un registro existente
@app.route("/vehicle_snap/<int:id_input>", methods=["PUT"])
def update_vehicle_snap(id_input):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE vehicle_snap SET class=%s, count_value=%s WHERE id_input=%s",
        (data["class"], data["count_value"], id_input)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Registro actualizado"})

# DELETE: eliminar un registro
@app.route("/vehicle_snap/<int:id_input>", methods=["DELETE"])
def delete_vehicle_snap(id_input):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicle_snap WHERE id_input=%s", (id_input,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Registro eliminado"})

# ------------------ Servidor ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
