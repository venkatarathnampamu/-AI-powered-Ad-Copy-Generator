from flask import Flask
from flask_cors import CORS
from routes import api_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_bp, url_prefix="/api")


@app.route("/")
def home():
    return {"message": "AI Ad Copy Generator API is running.", "version": "1.0.0"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
