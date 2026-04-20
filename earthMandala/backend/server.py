from flask import Flask, send_file, make_response, request
from flask_cors import CORS
import geoGen
import os
import uuid

app = Flask(__name__)
CORS(app)

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def parse_colors(color_str):
    """Parse comma-separated hex colors into list of RGB tuples. Returns None if invalid."""
    try:
        parts = color_str.split(",")
        if len(parts) != 3:
            return None
        colors = [(255, 255, 255)]
        for hex_color in parts:
            hex_color = hex_color.strip().lstrip("#")
            if len(hex_color) != 6:
                return None
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            colors.append((r, g, b))
        return colors
    except (ValueError, IndexError):
        return None

@app.route("/generate")
def generate():
    q_type = request.args.get("type", "sixteens")
    color_str = request.args.get("colors")

    colors = None
    if color_str:
        colors = parse_colors(color_str)
        if colors is None:
            return "Invalid colors parameter", 400

    filepath = f"{IMAGE_DIR}/{uuid.uuid4().hex}.jpg"
    try:
        geoGen.runGenerate(filepath, q_type, colors=colors)
        response = make_response(send_file(filepath, mimetype="image/jpeg"))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        return response
    except Exception as e:
        print(f"[!] Generation failed: {e}")
        return "Generation failed", 500
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
