from flask import Flask, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('init_match')
def init_match(data):
    print('We got info for a new match!')
    print(data)
    socketio.emit('init_match', data)

@socketio.on('update_match')
def update_match(data):
    print('We are trying to send (Async -> Client):')
    print(data)

    socketio.emit('update_match', data)
    # socketio.emit('update_match', {'DONE': 'DONE'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)