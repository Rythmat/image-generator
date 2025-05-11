from flask import Flask, send_file
from flask_cors import CORS
import gridGen
import threading
import time
import os
import uuid
from collections import deque

app = Flask(__name__)
CORS(app)

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

BUFFER_SIZE = 4
image_queue = deque()
queue_lock = threading.Lock()
current_image = None 

def generate_image_to_file(filepath):
    gridGen.runGridGen()
    os.rename("grid.png", filepath)

def image_producer():
    while True:
        with queue_lock:
            if len(image_queue) < BUFFER_SIZE:
                filename = f"{IMAGE_DIR}/grid_{uuid.uuid4().hex}.png"
                try:
                    generate_image_to_file(filename)
                    image_queue.append(filename)
                    print(f"[+] Generated and queued: {filename}")
                except Exception as e:
                    print("[-] Failed to generate image:", e)
        time.sleep(1)

def image_rotator():
    global current_image
    while True:
        with queue_lock:
            if image_queue:
                old_image = current_image
                current_image = image_queue.popleft()
                print(f"[→] Rotated to: {current_image}")
                if old_image and os.path.exists(old_image):
                    os.remove(old_image)
        time.sleep(5)

@app.route("/generate")
def generate():
    with queue_lock:
        if current_image and os.path.exists(current_image):
            return send_file(current_image, mimetype="image/png")
    return "No image ready yet", 503

if __name__ == "__main__":
    threading.Thread(target=image_producer, daemon=True).start()
    threading.Thread(target=image_rotator, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
