import random
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "aquaguard-codenova-secret-key"
DB_PATH = "aquaguard.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            location_id TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT DEFAULT 'Monitored Zone'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            sensor_id TEXT PRIMARY KEY,
            location_id TEXT NOT NULL,
            normal_flow REAL NOT NULL,
            scenario TEXT DEFAULT 'normal'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            flow_rate REAL NOT NULL,
            pressure REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS block_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            user_name TEXT NOT NULL,
            current_location TEXT NOT NULL,
            requested_location TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        INSERT OR IGNORE INTO users (email, name, password, role, location_id)
        VALUES (?, ?, ?, ?, ?)
    """, ("admin@aquaguard.org", "AquaGuard Admin", "admin123", "admin", None))

    cur.execute("""
        INSERT OR IGNORE INTO users (email, name, password, role, location_id)
        VALUES (?, ?, ?, ?, ?)
    """, ("manager@aquaguard.org", "Campus Manager", "manager123", "management", None))

    default_locations = [
        ("Main Gate Inlet", "Tank / Pump House"),
        ("Hostel Block A", "Residential Block"),
        ("Hostel Block B Tank", "Tank / Pump House"),
        ("Mess & Kitchen", "Cafeteria / Utility")
    ]
    for loc_name, loc_type in default_locations:
        cur.execute("INSERT OR IGNORE INTO locations (name, type) VALUES (?, ?)", (loc_name, loc_type))

    conn.commit()
    conn.close()


init_db()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ---------------- AUTHENTICATION ROUTES ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    selected_role = (data.get("role") or "").strip().lower()

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user or user["password"] != password:
        return jsonify({"success": False, "error": "Invalid email or password."}), 401

    if selected_role and user["role"] != selected_role:
        return jsonify({
            "success": False,
            "error": f"This account is registered under '{user['role']}', not '{selected_role}'."
        }), 403

    session_user = {
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "location_id": user["location_id"]
    }
    session["user"] = session_user
    return jsonify({"success": True, "user": session_user}), 200


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    location_id = (data.get("location_id") or "").strip()

    if not name or not email or not password or not location_id:
        return jsonify({"success": False, "error": "All fields including Block / Location are required."}), 400

    conn = get_db()
    existing = conn.execute("SELECT email FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({"success": False, "error": "Email already registered. Please sign in."}), 409

    conn.execute(
        "INSERT INTO users (email, name, password, role, location_id) VALUES (?, ?, ?, ?, ?)",
        (email, name, password, "resident", location_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Resident registered successfully."}), 201


@app.route("/api/me", methods=["GET"])
def get_current_user():
    sess_user = session.get("user")
    if not sess_user:
        return jsonify({"success": False, "user": None}), 401

    # Always refresh location_id from DB in case an Admin approved a block transfer
    conn = get_db()
    row = conn.execute("SELECT email, name, role, location_id FROM users WHERE email = ?", (sess_user["email"],)).fetchone()
    conn.close()
    if row:
        updated_user = dict(row)
        session["user"] = updated_user
        return jsonify({"success": True, "user": updated_user}), 200

    return jsonify({"success": True, "user": sess_user}), 200


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    if request.method == "POST":
        return jsonify({"success": True, "message": "Logged out"}), 200
    return redirect(url_for("login"))


# ---------------- BLOCK TRANSFER REQUESTS (RESIDENT -> ADMIN) ----------------

@app.route("/api/block-requests", methods=["GET", "POST"])
def api_block_requests():
    conn = get_db()
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        email = (data.get("user_email") or "").strip().lower()
        name = (data.get("user_name") or "").strip()
        curr_loc = (data.get("current_location") or "").strip()
        req_loc = (data.get("requested_location") or "").strip()
        reason = (data.get("reason") or "").strip()

        if not email or not req_loc:
            conn.close()
            return jsonify({"success": False, "error": "Requested block is required."}), 400

        if curr_loc.lower() == req_loc.lower():
            conn.close()
            return jsonify({"success": False, "error": "You are already assigned to this block."}), 400

        ts = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        conn.execute("""
            INSERT INTO block_requests (user_email, user_name, current_location, requested_location, reason, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'pending', ?)
        """, (email, name, curr_loc, req_loc, reason, ts))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Block transfer request sent to Admin."}), 201

    rows = conn.execute("SELECT * FROM block_requests ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify({"success": True, "requests": [dict(r) for r in rows]})


@app.route("/api/block-requests/<int:req_id>/decision", methods=["POST"])
def api_block_request_decision(req_id):
    data = request.get_json(silent=True) or {}
    decision = (data.get("decision") or "").strip().lower()
    if decision not in ("approved", "rejected"):
        return jsonify({"success": False, "error": "Invalid decision"}), 400

    conn = get_db()
    req_row = conn.execute("SELECT * FROM block_requests WHERE id = ?", (req_id,)).fetchone()
    if not req_row:
        conn.close()
        return jsonify({"success": False, "error": "Request not found"}), 404

    conn.execute("UPDATE block_requests SET status = ? WHERE id = ?", (decision, req_id))
    if decision == "approved":
        conn.execute("UPDATE users SET location_id = ? WHERE email = ?", (req_row["requested_location"], req_row["user_email"]))

    conn.commit()
    conn.close()
    return jsonify({"success": True, "status": decision})


# ---------------- SENSOR, NIGHT LEAK & LOCATION APIS ----------------

@app.route("/api/locations", methods=["GET", "POST"])
def api_locations():
    conn = get_db()
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = (data.get("name") or "").strip()
        loc_type = (data.get("type") or "Monitored Zone").strip()
        if not name:
            conn.close()
            return jsonify({"success": False, "error": "Location name required"}), 400
        conn.execute("INSERT OR IGNORE INTO locations (name, type) VALUES (?, ?)", (name, loc_type))
        conn.commit()

    rows = conn.execute("SELECT name, type FROM locations ORDER BY id ASC").fetchall()
    conn.close()
    return jsonify({"success": True, "locations": [dict(r) for r in rows]})


@app.route("/api/sensors", methods=["GET", "POST"])
def api_sensors():
    conn = get_db()
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        sensor_id = (data.get("sensor_id") or "").strip()
        location_id = (data.get("location_id") or "").strip()
        normal_flow = float(data.get("normal_flow") or 45.0)

        if not sensor_id or not location_id:
            conn.close()
            return jsonify({"success": False, "error": "Sensor ID and Location are required"}), 400

        conn.execute(
            "INSERT OR IGNORE INTO sensors (sensor_id, location_id, normal_flow, scenario) VALUES (?, ?, ?, 'normal')",
            (sensor_id, location_id, normal_flow)
        )
        conn.execute("INSERT OR IGNORE INTO locations (name, type) VALUES (?, 'Monitored Zone')", (location_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True}), 201

    rows = conn.execute("SELECT sensor_id, location_id, normal_flow, scenario FROM sensors ORDER BY sensor_id ASC").fetchall()
    conn.close()
    return jsonify({"success": True, "sensors": [dict(r) for r in rows]})


@app.route("/api/sensors/<sensor_id>/scenario", methods=["POST"])
def api_sensor_scenario(sensor_id):
    data = request.get_json(silent=True) or {}
    scenario = (data.get("scenario") or "normal").strip()
    conn = get_db()
    conn.execute("UPDATE sensors SET scenario = ? WHERE sensor_id = ?", (scenario, sensor_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "sensor_id": sensor_id, "scenario": scenario})


@app.route("/api/sensors/<sensor_id>/readings", methods=["GET", "POST"])
def api_sensor_readings(sensor_id):
    conn = get_db()
    sensor = conn.execute("SELECT * FROM sensors WHERE sensor_id = ?", (sensor_id,)).fetchone()
    if not sensor:
        conn.close()
        return jsonify({"success": False, "error": "Sensor not found", "readings": []}), 404

    if request.method == "POST":
        base = float(sensor["normal_flow"])
        scen = sensor["scenario"]
        now_dt = datetime.now()

        if scen in ("burst", "burst_leak"):
            flow = round(base * random.uniform(2.1, 2.5), 1)
            pressure = round(random.uniform(0.9, 1.3), 1)
            ts = now_dt.strftime("%Y-%m-%d %I:%M:%S %p")
        elif scen == "night_leak":
            # Simulates Minimum Night Flow (MNF) between 02:00 AM and 04:00 AM when normal usage should be ~0 L/hr
            flow = round(base * random.uniform(0.75, 1.15), 1)
            pressure = round(random.uniform(1.6, 1.9), 1)
            night_min = random.randint(10, 55)
            night_hour = random.choice(["02", "03"])
            ts = now_dt.strftime(f"%Y-%m-%d {night_hour}:{night_min:02d}:00 AM (Night 2-4 AM)")
        elif scen in ("continuous_leak", "leak"):
            flow = round(base * random.uniform(1.45, 1.75), 1)
            pressure = round(random.uniform(1.5, 1.8), 1)
            ts = now_dt.strftime("%Y-%m-%d %I:%M:%S %p")
        elif scen in ("gradual_leak", "gradual"):
            flow = round(base * random.uniform(1.25, 1.45), 1)
            pressure = round(random.uniform(1.8, 2.0), 1)
            ts = now_dt.strftime("%Y-%m-%d %I:%M:%S %p")
        else:
            flow = round(base * random.uniform(0.95, 1.05), 1)
            pressure = round(random.uniform(2.1, 2.3), 1)
            ts = now_dt.strftime("%Y-%m-%d %I:%M:%S %p")

        conn.execute(
            "INSERT INTO readings (sensor_id, flow_rate, pressure, timestamp) VALUES (?, ?, ?, ?)",
            (sensor_id, flow, pressure, ts)
        )
        conn.commit()
        conn.close()
        return jsonify({
            "success": True,
            "reading": {"sensor_id": sensor_id, "flow_rate": flow, "pressure": pressure, "timestamp": ts}
        })

    rows = conn.execute(
        "SELECT sensor_id, flow_rate, pressure, timestamp FROM readings WHERE sensor_id = ? ORDER BY id ASC LIMIT 50",
        (sensor_id,)
    ).fetchall()
    conn.close()
    return jsonify({"success": True, "readings": [dict(r) for r in rows]})


# ---------------- PAGE ROUTES ----------------

@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/sensors")
@login_required
def sensors():
    return render_template("sensors.html")


@app.route("/readings")
@login_required
def readings():
    return render_template("readings.html")


@app.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html")


@app.route("/alerts")
@login_required
def alerts():
    return render_template("alerts.html")


@app.route("/inspection")
@login_required
def inspection():
    return render_template("inspection.html")


@app.route("/locations")
@login_required
def locations():
    return render_template("locations.html")


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True)