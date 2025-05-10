from flask import Flask, send_file
from flask_cors import CORS
import gridGen
import threading
import time, os

app = Flask(__name__)
CORS(app)

image_path = "grid.png"

def auto_update_image():
    while True:
        try:
            gridGen.runGridGen()
            print("Image updated.")
        except Exception as e:
            print("Failed to update image:", e)
        time.sleep(5)

@app.route("/generate")
def generate():
    if os.path.exists(image_path):
        return send_file(image_path, mimetype="image/png")
    return "Image not yet generated", 503

if __name__ == "__main__":
    thread = threading.Thread(target=auto_update_image, daemon=True)
    thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)