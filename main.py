from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
import subprocess

app = Flask(__name__)
OUTPUT_FOLDER = "output"

@app.route("/cut", methods=["POST"])
def cut():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    uid = str(uuid.uuid4())
    input_path = f"temp_{uid}.mp4"
    file.save(input_path)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_pattern = os.path.join(OUTPUT_FOLDER, "clip_%03d.mp4")
    command = f"ffmpeg -i {input_path} -c copy -map 0 -segment_time 25 -f segment {output_pattern}"
    subprocess.call(command, shell=True)

    os.remove(input_path)

    clips = sorted(os.listdir(OUTPUT_FOLDER))
    urls = [f"/output/{clip}" for clip in clips if clip.endswith(".mp4")]

    return jsonify({"status": "ok", "clips": urls})

@app.route("/output/<filename>")
def serve_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
 
