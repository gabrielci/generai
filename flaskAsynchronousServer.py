from flask import Flask
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Testing
@socketio.on('connect')
def sendDataIO():
    print ("You got here")
    # Se manda el numero del jugador (0 a 2)
    print("Shall we load shiet?: ")
    answer = input()

    # Se manda la jugada:
    # '4'
    # '5
    # '6'
    # 'straight'
    # 'fullhouse'
    # 'four_of_a_kind'
    # 'yahtzee'
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

if __name__ == '__main__':
    socketio.run(app)


#@socketio.on('my_event')
# var['key']
# var.get('key', valor_por_default)
