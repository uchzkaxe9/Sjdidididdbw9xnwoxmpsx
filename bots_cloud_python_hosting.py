from flask import Flask, render_template, request, jsonify import subprocess import os

app = Flask(name) UPLOAD_FOLDER = "uploaded_bots" os.makedirs(UPLOAD_FOLDER, exist_ok=True)

bots = {}

Route: Home Page

@app.route('/') def index(): return render_template('index.html', bots=bots)

Route: Upload Bot File and Token

@app.route('/upload', methods=['POST']) def upload(): if 'bot_file' not in request.files or 'bot_token' not in request.form: return jsonify({'error': 'Missing file or bot token'}), 400

bot_file = request.files['bot_file']
bot_token = request.form['bot_token']

if bot_file.filename == '':
    return jsonify({'error': 'No selected file'}), 400

bot_path = os.path.join(UPLOAD_FOLDER, bot_file.filename)
bot_file.save(bot_path)

process = subprocess.Popen(["nohup", "python", bot_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
bots[bot_file.filename] = {'token': bot_token, 'pid': process.pid, 'status': 'Running'}

return jsonify({'message': 'Bot hosted successfully', 'bot_name': bot_file.filename})

Route: Check Running Bots Status

@app.route('/status') def status(): return jsonify(bots)

Route: Stop a Running Bot

@app.route('/stop/<bot_name>', methods=['POST']) def stop(bot_name): if bot_name in bots: try: os.kill(bots[bot_name]['pid'], 9) bots[bot_name]['status'] = 'Stopped' return jsonify({'message': 'Bot stopped successfully'}) except Exception as e: return jsonify({'error': str(e)}), 500 return jsonify({'error': 'Bot not found'}), 404

if name == 'main': app.run(host='0.0.0.0', port=5000, debug=True)

