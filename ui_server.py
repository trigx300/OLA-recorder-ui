from flask import Flask, render_template, request, jsonify
import subprocess
import os
import logging
import re

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

# Define the base directory
BASE_DIR = os.path.join(os.path.expanduser('~'), 'ola_recorder_ui')
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)  # Create the directory if it doesn't exist

app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"  # Placeholder for your HTML return

@app.route('/list_art_files')
def list_art_files():
    files = [f for f in os.listdir(BASE_DIR) if f.endswith('.art')]
    return jsonify(files=files)

@app.route('/record', methods=['POST'])
def record():
    data = request.json
    action = data.get('action')
    filename = os.path.join(BASE_DIR, data.get('filename', 'default') + '.art')
    universe = data.get('universe', '0')  # Default to '0' if not provided

    if action == 'start':
        cmd = ["ola_recorder", "-r", filename, "-u", universe]
    elif action == 'stop':
        cmd = ["ola_recorder", "--stop", "-u", universe]
    else:
        return jsonify({'error': 'Invalid action'}), 400

    logging.debug(f"Executing command: {' '.join(cmd)}")
    
    try:
        if action == 'stop':
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
            match = re.search(r'Saved (\d+) frames', output)
            frame_count = int(match.group(1)) if match else 0
            return jsonify({'message': 'Stopped recording', 'frameCount': frame_count}), 200
        else:
            subprocess.Popen(cmd)
            return jsonify({'message': f"{action.capitalize()}ing recording"}), 200
    except subprocess.CalledProcessError as e:
        logging.error(f'Error executing command: {e.output.decode()}')
        return jsonify({'error': 'Error executing command'}), 500

@app.route('/play', methods=['POST'])
def play():
    data = request.get_json()
    action = data.get('action')
    filename = os.path.join(BASE_DIR, data.get('filename', '').strip() + '.art')
    universe = data.get('universe')

    cmd = ["ola_recorder", "-p", filename, "-u", universe, "-i", "0"] if action == 'start' else ["pkill", "ola_recorder"]

    logging.debug(f"Executing command: {' '.join(cmd)}")
    subprocess.Popen(cmd)
    return jsonify({'message': f"Playback {action}ed for {filename} on universe {universe}"}), 200

@app.route('/rename_file', methods=['POST'])
def rename_file():
    data = request.get_json()
    old_name = os.path.join(BASE_DIR, data.get('filename') + '.art')
    new_name = os.path.join(BASE_DIR, data.get('newname') + '.art')

    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        return jsonify({'message': "File renamed successfully"}), 200
    else:
        return jsonify({'error': "File not found"}), 404

@app.route('/delete_file', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = os.path.join(BASE_DIR, data.get('filename') + '.art')

    if os.path.exists(filename):
        os.remove(filename)
        return jsonify({'message': "File deleted successfully"}), 200
    else:
        return jsonify({'error': "File not found"}), 404
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
