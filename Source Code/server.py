import wave
import io
import time
import json
from flask import Flask, request, jsonify, g, render_template
from flask_socketio import SocketIO, emit
import socket
import requests
import os
# from spectral import remove_beats
from noise_reduce_final import noise_reduce
from mel import mel
from high_pass import remove_heartbeats

print("IN - TRAINING")
from cwnone import predict

hostname = socket.gethostname()

ip_address = "192.168.202.230"
esp_ip = "192.168.76.71"

print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

app = Flask(__name__)
socketio = SocketIO(app)
connected_clients = []

def load_temperatures():
    try:
        with open('/data.json', 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []

temperatures = load_temperatures()


def download_audio_file(url, save_folder, file_name):
    # Ensure the folder exists
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    save_path = os.path.join(save_folder, file_name)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Audio file downloaded successfully to {save_path}")
    else:
        print(f"Failed to download audio file. Status code: {response.status_code}")


def save_temperatures():
    with open('/data.json', 'w') as json_file:  
        json.dump(temperatures, json_file)

current_audio_file = "audio-" + str(int(time.time()))

uploading_state = False
client_user = 0

@app.route("/start-audio", methods=['GET'])
def start_audio():
    print("Hello")
    global uploading_state
    global current_audio_file

    if not uploading_state:
        current_audio_file = "audio-"+str(int(time.time()))
    uploading_state = True
    
    print(request)

    socketio.emit("message", {"text": "Recording started.."}, room=client_user)
    return "Header received", 200

@app.route('/stop-audio')
def stopAudio():

    global uploading_state
    global client_user

    uploading_state = False
    print(f"Audio file uploaded and saved as '{current_audio_file}.wav'")

    audio_url = f"http://{esp_ip}/recording.wav"
    save_path = "" 

    download_audio_file(audio_url, "static", f"{current_audio_file}.wav")

    print("Removing beat noises..")

    # without beats
    # remove_beats(file_path, f"{current_audio_file}_wob.wav")

    if client_user:
        socketio.emit("audio-file", {"file_name": f"{current_audio_file}.wav"}, room=client_user)
        client_user = 0
    
    return "Saved as an audio file!", 200

@app.route('/post-data', methods=['POST'])
def post_data():
    try:
        data = request.get_json()
        # data_type = data.get('type')
        data_value = data.get('header64')
        
        timestamp = int(time.time())
        response_message = f"Received data: Value='{data_value}' Time={timestamp}"
        
        # if data_type == "temp":
        temperatures.append([timestamp, float(data_value)])
        save_temperatures()

        return jsonify({"message": response_message}), 200
    except Exception as e:
        return str(e), 500

@socketio.on("connect")
def handle_socket_connect():
    global uploading_state
    
    connected_clients.append(request.sid)

    if uploading_state:
        socketio.emit("message", {"text": "Recorder is being used by other user, Please try again after some time."}, room=request.sid)
        
@socketio.on("disconnect")
def handle_disconnect():
    if not connected_clients:
        client_user = 0
    if request.sid == client_user:
        client_user = 0
    if request.sid in connected_clients:
        connected_clients.remove(request.sid)
    

@socketio.on("start-recording")
def start_recording():
    global uploading_state
    global client_user
    
    client_id = request.sid
    client_user = client_id

    if uploading_state:
        socketio.emit("message", {"text": "Recorder is being used by other user, Please try again after some time."}, room=client_id)

@socketio.on("give-mel")
def give_mel(audio_file):

    print('hello')
    audio_file = audio_file["file_name"]
    image_file = mel(audio_file)


    socketio.emit("mel", {"text": "Mel successful!", "image": image_file})

@socketio.on("noise-reduce")
def reduce_noise(audio_file):
    audio_file = audio_file["file_name"]
    red_file = noise_reduce(audio_file)
    image_file = mel(red_file)

    socketio.emit("reduce-mel", {"text": "Noise reduction success", "image": image_file})

@socketio.on("remove-hb")
def remove_hb(audio_file):
    audio = audio_file["file_name"]
    red_file = remove_heartbeats(audio)
    image_file = mel(red_file)
    print(red_file, image_file)

    socketio.emit("remove-hb-mel", {"text": "Removing heartbeat: Success!", "image": image_file})

@socketio.on("give-class")
def give_class(audio_file):
    audio_file = audio_file["file_name"]
    class_ = predict(audio_file)

    print("Class: ", class_)
    
    socketio.emit("take-class", {"class": class_, "text": "Classification: Success!"})

@socketio.on("add-file-to-user")
def addToJson(ctx):

    file_name = ctx["file-name"]
    name = ctx["user"]

    data = {}
    with open("recordings.json", "r") as json_file:
        data = json.load(json_file)
        if name in data:
            data[name].append(file_name)
        else:
            data[name] = [file_name]
        print(ctx)
    
    with open("recordings.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

import sqlite3

app.config['DATABASE'] = 'mydatabase.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
from flask import Flask, render_template


@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/admin.html')
def admin():
    return render_template('admin.html')


@app.route('/admin1.html')
def admin1():
    return render_template('admin1.html')

@app.route('/livetemperature.html')
def livetemperature():
    return render_template('livetemperature.html')

@app.route('/test.html')
def test():
    return render_template('test.html')

@app.route('/user.html')
def user():
    return render_template('user.html')

@app.route('/login', methods=['POST'])
def userhome():
    db = get_db()
    cursor = db.cursor()

    data = request.form
    username = data.get("username")
    password = data.get("password")

    command = f"SELECT name, age from users WHERE username= ? AND password = ?;"
    cursor.execute(command, (username, password,))
    result = cursor.fetchall()
    if not result:
        return render_template("user.html")
    name = result[0][0]
    age = result[0][1]
    
    data_array = {}
    with open("recordings.json", "r") as json_file:
        data_array = json.load(json_file)

    audio_array = []
    if name in data_array:
        audio_array = data_array[name]
    return render_template('userhome.html', name=name, age=age, data_array=audio_array)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    db = get_db()
    cursor = db.cursor()

    username = request.form['newUsername']
    password = request.form['newPassword']
    name = request.form['name']
    age = request.form['age']
    voice_recording = "lite"

    cursor.execute("INSERT INTO users (username, password, name, age, voiceRecording) VALUES (?, ?, ?, ?, ?)",
                    (username, password, name, age, voice_recording))

    db.commit()

    return 'Data submitted successfully'

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host=ip_address)
