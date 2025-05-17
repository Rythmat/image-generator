from flask import Flask, send_file, make_response, request
from flask_cors import CORS
# import gridGen
import geoGen
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
queues = {
    "eights": deque(),
    "sixteens": deque(),
    "thirtytwos": deque()
}
queue_lock = threading.Lock()
current_images = {
  "eights": None,
  "sixteens": None,
  "thirtytwos": None
}

recent_images = {
  "eights": deque(maxlen=5),
  "sixteens": deque(maxlen=5),
  "thirtytwos": deque(maxlen=5)
}

deque(maxlen=5) 

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

def generate_async(filepath, type):
    try:
        # gridGen.runGridGen(filepath)
        geoGen.runGenerate(filepath, type)
        with queue_lock:
            queues[type].append(filepath)
            print(f"[+] Queued image: {filepath}")
    except Exception as e:
        print(f"[!] Image generation failed: {e}")

def image_producer():
    while True:
        with queue_lock:
            for type, queue in queues.items():
                if len(queue) < BUFFER_SIZE:
                    filename = f"{IMAGE_DIR}/{type}_{uuid.uuid4().hex}.png"
                    executor.submit(generate_async, filename, type)
        time.sleep(1)

def image_rotator(type):
    while True:
        with queue_lock:
            queue = queues[type]
            if queue:
                old_image = current_images[type]
                current_images[type] = queue.popleft()
                recent_images[type].append(old_image)
                print(f"[→] Rotated to: {current_images[type]}")
            while len(recent_images[type]) > 2:
                img_to_delete = recent_images[type].popleft()
                if img_to_delete and os.path.exists(img_to_delete):
                    try:
                        os.remove(img_to_delete)
                        print(f"[✖] Deleted old image: {img_to_delete}")
                    except Exception as e:
                        print(f"[!] Failed to delete image: {e}")
        time.sleep(5)

@app.route("/generate")
def generate():
    q_type = request.args.get("type", "sixteens")
    with queue_lock:
        if q_type in current_images:
            img = current_images[q_type]
            if img and os.path.exists(img):
                response = make_response(send_file(img, mimetype="image/png"))
                response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
                return response
    return "No image ready yet", 503

if __name__ == "__main__":
    threading.Thread(target=image_producer, daemon=True).start()
    for type in queues:
        threading.Thread(target=image_rotator, args=(type,), daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
