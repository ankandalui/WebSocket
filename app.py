from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')




# Dictionary to store the latest output from each client
client_data = {}

@app.route('/')
def index():
    return "Socket.IO Server is running"

@socketio.on('client_data')
def handle_client_data(data):
    client_id = data['client_id']
    output = data['output']
    client_data[client_id] = output
    print(f"Received data from Client {client_id}: {output}")
    emit('update_data', {'client_id': client_id, 'output': output}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)