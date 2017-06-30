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


# When a client connects we must emit the match initialization and current moves if they exist
@socketio.on('client_connect')
def status_match():
    global init_info
    global status_info

    print('Someone got connected')

    if len(init_info) != 0:
        print('We are trying to send initial match data (Async Server -> Client):')
        print(init_info)
        socketio.emit('init_match', init_info)

    if len(status_info) != 0:
        print('We are trying to send match status (Async Server -> Client):')
        print(init_info)
        socketio.emit('status_match', status_info)


# When we recieve from the sync server that a match has started we must reset a couple of fields and broadcast the event
@socketio.on('init_match')
def init_match(data):
    global init_info
    global status_info
    init_info = data
    status_info = []

    print('A new match has begun')
    print('We are trying to send initial match data (Async Server -> Client):')
    print(data)
    socketio.emit('init_match', data)


# When we recieve a new move from the sync server we must append it to the total moves made list and broadcast the move
@socketio.on('update_match')
def update_match(data):
    global status_info
    status_info.append(data)

    print('We are trying to send match update (Async Server -> Client):')
    print(data)
    socketio.emit('update_match', data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)