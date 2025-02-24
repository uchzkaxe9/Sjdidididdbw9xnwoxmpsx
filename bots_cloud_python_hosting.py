from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = "bots"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "bot_file" not in request.files or "bot_token" not in request.form:
        return jsonify({"error": "File and Bot Token required!"}), 400

    bot_file = request.files["bot_file"]
    bot_token = request.form["bot_token"]

    if bot_file.filename == "":
        return jsonify({"error": "No selected file!"}), 400

    bot_path = os.path.join(UPLOAD_FOLDER, bot_file.filename)
    bot_file.save(bot_path)

    try:
        subprocess.Popen(["nohup", "python3", bot_path, bot_token], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({"success": "Bot Hosted Successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
