from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import os
import subprocess
import yaml
import json

app = Flask(__name__)
app.secret_key = 'qwertyuiop' 

YAML_FILES = {
    "10080_Config": "./static/codes/SFB_10080.yaml",
    "22880_Config": "./static/codes/SFB_22880.yaml"
}

EXE_PATHS = {
    "10080": "./static/codes/SFB_10080.exe",
    "22880": "./static/codes/SFB_22880.exe"
}

credentials = {
    'admin': 'password',
    'Kanchan': 'Kanchan123',
    'Asif': 'Asif123',
    'Tasdeeque': 'Tasdeeque123'
}

class QuotedString(str):
    pass

def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

yaml.add_representer(QuotedString, quoted_presenter)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if credentials.get(username) == password:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.", "error")

    return render_template('login.html')

@app.route('/get_yaml', methods=['GET'])
def get_yaml():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    file_key = request.args.get('file_key')
    file_path = YAML_FILES.get(file_key)
    if not file_path:
        return jsonify({"error": "Invalid file key"}), 400
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return jsonify({"content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save_yaml', methods=['POST'])
def save_yaml():
    data = request.json
    file_key = data.get('file_key')
    new_content = data.get('content')
    file_path = YAML_FILES.get(file_key)
    
    if not file_path:
        return jsonify({"error": "Invalid file key"}), 400

    try:
        parsed_data = yaml.safe_load(new_content)
        for key in parsed_data.keys():
            if isinstance(parsed_data[key], str):
                parsed_data[key] = QuotedString(parsed_data[key])

        with open(file_path, 'w') as file:
            yaml.dump(parsed_data, file, allow_unicode=True)
        return jsonify({"message": "File saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/edit_config')
def edit_config():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('edit_config.html')

@app.route('/execute_sfb_process', methods=['POST'])
def execute_sfb_process():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    data = request.json
    process = data.get("process")
    exe_paths = EXE_PATHS
    
    if process not in exe_paths:
        return jsonify({"error": "Invalid process selected"}), 400
    
    exe_path = exe_paths[process]
    
    try:
        result = subprocess.run([exe_path], capture_output=True, text=True, check=True)
        return jsonify({"output": result.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Execution failed: {e.stderr}"}), 500

@app.route('/run_exe', methods=['GET'])
def run_exe():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('run_exe.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
