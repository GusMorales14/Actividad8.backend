from flask import Flask, request, jsonify
import mysql.connector

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "contrasena",  # <-- cámbialo si tu contenedor usa 'constrasena'
    "database": "trafico",
    "port": 3306,
}

app = Flask(__name__)

def get_conn():
    return mysql.connector.connect(**db_config)

# --------- LISTAR (GET /vehicle_snap) ----------
@app.route("/vehicle_snap", methods=["GET"])
def list_vehicle_snap():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM vehicle_snap ORDER BY id ASC")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify(rows)

# --------- OBTENER POR ID (GET /vehicle_snap/<id>) ----------
@app.route("/vehicle_snap/<int:id_input>", methods=["GET"])
def get_vehicle_snap_by_id(id_input):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM vehicle_snap WHERE id=%s", (id_input,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if row:
        return jsonify(row)
    return jsonify({"error": "Registro no encontrado"}), 404

# --------- CREAR (POST /vehicle_snap) ----------
@app.route("/vehicle_snap", methods=["POST"])
def create_vehicle_snap():
    data = request.json or {}
    required = ["car_count", "truck_count", "motorcycle_count", "bus_count", "total_count"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Faltan campos: {missing}"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO vehicle_snap
        (car_count, truck_count, motorcycle_count, bus_count, total_count)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data["car_count"],
            data["truck_count"],
            data["motorcycle_count"],
            data["bus_count"],
            data["total_count"],
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close(); conn.close()
    return jsonify({"id": new_id, "message": "Creado"}), 201

# --------- ACTUALIZAR (PUT /vehicle_snap/<id>) ----------
@app.route("/vehicle_snap/<int:id_input>", methods=["PUT"])
def update_vehicle_snap(id_input):
    data = request.json or {}
    required = ["car_count", "truck_count", "motorcycle_count", "bus_count", "total_count"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Faltan campos: {missing}"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE vehicle_snap
        SET car_count=%s, truck_count=%s, motorcycle_count=%s, bus_count=%s, total_count=%s
        WHERE id=%s
        """,
        (
            data["car_count"],
            data["truck_count"],
            data["motorcycle_count"],
            data["bus_count"],
            data["total_count"],
            id_input,
        ),
    )
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"message": "Actualizado"})

# --------- BORRAR (DELETE /vehicle_snap/<id>) ----------
@app.route("/vehicle_snap/<int:id_input>", methods=["DELETE"])
def delete_vehicle_snap(id_input):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM vehicle_snap WHERE id=%s", (id_input,))
    conn.commit()
    cur.close(); conn.close()
    return jsonify({"message": "Eliminado"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
