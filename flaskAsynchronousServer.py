from flask import Flask, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# Testing
@socketio.on('test')
def run_test(data):
    print('We got the message:')

    print(data['data'])


@socketio.on('update_state')
def send_data_io(data):
    message = {'players': ['CONIO', 'SERIAL'], 'scoresheet_n': 2}
    print('Message and Data to send')
    print(message)
    print(data)

    socketio.emit('update_state', data)
    socketio.emit('update_state', {'DONE': 'DONE'})
    '''
    # Currently its generating plays for every box and sending them to the clients
    
    av_plays = ['_4', '_5', '_6', '_straight', '_fullhouse', '_four_of_a_kind', '_yahtzee']
    for player_turn in range(0, 3):
        for scoresh in range(0, 3):
            for play in av_plays:
                if play == '_4' or play == '_5' or play == '_6':
                    mult = random.randint(0, 5)
                    message = {'player': player_turn, 'scoresheet': scoresh, 'play': play, 'multiplier': mult,
                               'bonus': 0}
                else:
                    mult = random.randint(0, 1)
                    bon = random.randint(0, 1)
                    message = {'player': player_turn, 'scoresheet': scoresh, 'play': play, 'multiplier': mult,
                               'bonus': bon*mult}

                print('Se envia: ')
                print(message)
                emit('update_state', message)
    

    
    emit('update_state', {'DONE': 'DONE'})
    '''

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)