from flask import Flask
from backend.routes.sensor import sensor_bp

app = Flask(__name__)
app.register_blueprint(sensor_bp)

if __name__ == "__main__":
    app.run(debug=True)