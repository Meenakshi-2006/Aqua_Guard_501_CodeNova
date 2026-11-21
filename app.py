
from flask import Flask, render_template
from backend.routes.dashboard import dashboard_bp

app = Flask(__name__)

app.register_blueprint(dashboard_bp)

# =====================================
# AQUAGUARD - PAGE ROUTES
# =====================================

# 1. Dashboard
@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# 2. Virtual Sensors
@app.route("/sensors")
def sensors():
    return render_template("sensors.html")


# 3. Readings
@app.route("/readings")
def readings():
    return render_template("readings.html")


# 4. Analytics
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


# 5. Leak Alerts
@app.route("/alerts")
def alerts():
    return render_template("alerts.html")


# 6. Inspection
@app.route("/inspection")
def inspection():
    return render_template("inspection.html")


# 7. Locations
@app.route("/locations")
def locations():
    return render_template("locations.html")


# 8. Settings
@app.route("/settings")
def settings():
    return render_template("settings.html")


# =====================================
# RUN APPLICATION
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
