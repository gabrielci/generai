from flask import Flask, request
from flask_socketio import SocketIO, emit
import random

# Global variables containing current match status and the initialization stuff
init_info = {}
status_info = []

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('client_connect')
def status_match():
    global init_info
    global status_info

    print('Someone got connected')

    if len(init_info) != 0:
        socketio.emit('init_match', init_info)

    if len(status_info) != 0:
        socketio.emit('status_match', status_info)


@socketio.on('init_match')
def init_match(data):
    global init_info
    global status_info
    init_info = data
    status_info = []

    print('We got info for a new match!')
    print(data)
    socketio.emit('init_match', data)
    print('Data sent to others')

@socketio.on('update_match')
def update_match(data):
    global status_info
    status_info.append(data)

    socketio.emit('update_match', data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)