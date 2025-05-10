from flask import Flask, send_file
import gridGen
import time, os

app = Flask(__name__)

@app.route("/generate")
def generate():
    gridGen.runGridGen()

    return send_file("grid.png", mimetype="image/png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)