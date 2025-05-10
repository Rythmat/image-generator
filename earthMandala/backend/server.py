from flask import Flask, send_file
import gridGen
import time, os

app = Flask(__name__)

@app.route("/generate")
def generate():
    gridGen.runGridGen()

    return send_file("grid.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(port=5000)