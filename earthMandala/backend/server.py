from flask import Flask, send_file, make_response
from flask_cors import CORS
import gridGen
import threading
import time
import os
import uuid
from collections import deque
import concurrent.futures

app = Flask(__name__)
CORS(app)

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

BUFFER_SIZE = 5 
image_queue = deque()
queue_lock = threading.Lock()
current_image = None
recent_images = deque(maxlen=5) 

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

def generate_async(filepath):
    try:
        gridGen.runGridGen(filepath)
        with queue_lock:
            image_queue.append(filepath)
            print(f"[+] Queued image: {filepath}")
    except Exception as e:
        print(f"[!] Image generation failed: {e}")

def image_producer():
    while True:
        with queue_lock:
            if len(image_queue) < BUFFER_SIZE:
                filename = f"{IMAGE_DIR}/grid_{uuid.uuid4().hex}.png"
                executor.submit(generate_async, filename)
        time.sleep(1)

def image_rotator():
    global current_image
    while True:
        with queue_lock:
            if image_queue:
                old_image = current_image
                current_image = image_queue.popleft()
                recent_images.append(old_image)
                print(f"[→] Rotated to: {current_image}")

        with queue_lock:
            while len(recent_images) > 2:
                img_to_delete = recent_images.popleft()
                if img_to_delete and os.path.exists(img_to_delete):
                    try:
                        os.remove(img_to_delete)
                        print(f"[✖] Deleted old image: {img_to_delete}")
                    except Exception as e:
                        print(f"[!] Failed to delete image: {e}")
        time.sleep(5)

@app.route("/generate")
def generate():
    with queue_lock:
        if current_image and os.path.exists(current_image):
            response = make_response(send_file(current_image, mimetype="image/png"))
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            return response
    return "No image ready yet", 503

if __name__ == "__main__":
    threading.Thread(target=image_producer, daemon=True).start()
    threading.Thread(target=image_rotator, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
