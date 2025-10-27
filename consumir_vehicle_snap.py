# consumir_vehicle_snap.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000/vehicle_snap"
HEADERS = {"Content-Type": "application/json"}

def pretty(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

# ------- CRUD helpers -------

def list_snapshots():
    print("\n[GET] Lista de snapshots")
    r = requests.get(BASE_URL, timeout=10)
    print(f"Status: {r.status_code}")
    pretty(r.json())

def get_snapshot(snap_id: int):
    print(f"\n[GET] Snapshot id={snap_id}")
    r = requests.get(f"{BASE_URL}/{snap_id}", timeout=10)
    print(f"Status: {r.status_code}")
    try:
        pretty(r.json())
    except Exception:
        print(r.text)

def create_snapshot(car, truck, moto, bus):
    total = car + truck + moto + bus
    payload = {
        "car_count": car,
        "truck_count": truck,
        "motorcycle_count": moto,
        "bus_count": bus,
        "total_count": total
    }
    print("\n[POST] Crear snapshot")
    pretty(payload)
    r = requests.post(BASE_URL, headers=HEADERS, data=json.dumps(payload), timeout=10)
    print(f"Status: {r.status_code}")
    data = r.json()
    pretty(data)
    return data.get("id")

def update_snapshot(snap_id: int, car, truck, moto, bus):
    total = car + truck + moto + bus
    payload = {
        "car_count": car,
        "truck_count": truck,
        "motorcycle_count": moto,
        "bus_count": bus,
        "total_count": total
    }
    print(f"\n[PUT] Actualizar snapshot id={snap_id}")
    pretty(payload)
    r = requests.put(f"{BASE_URL}/{snap_id}", headers=HEADERS, data=json.dumps(payload), timeout=10)
    print(f"Status: {r.status_code}")
    try:
        pretty(r.json())
    except Exception:
        print(r.text)

def delete_snapshot(snap_id: int):
    print(f"\n[DELETE] Eliminar snapshot id={snap_id}")
    r = requests.delete(f"{BASE_URL}/{snap_id}", timeout=10)
    print(f"Status: {r.status_code}")
    try:
        pretty(r.json())
    except Exception:
        print(r.text or "{ }")

# ------- Demo secuencial para el video -------

if __name__ == "__main__":
    # 1) Listar existentes
    list_snapshots()

    # 2) Crear uno nuevo
    new_id = create_snapshot(car=12, truck=3, moto=5, bus=1)

    # 3) Consultarlo por ID
    if new_id:
        get_snapshot(new_id)

        # 4) Actualizarlo
        update_snapshot(new_id, car=10, truck=2, moto=4, bus=1)

        # 5) Consultar de nuevo
        get_snapshot(new_id)

        # 6) Borrarlo
        delete_snapshot(new_id)

    # 7) Listar para ver el estado final
    list_snapshots()
