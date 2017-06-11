from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Testing
@socketio.on('got connected')
def sendDataIO():
    # Se manda el numero del jugador (0 a 2)
    print("Input Player:")
    t1 = input()

    # Se manda el numero del scoresheet (0 a 2)
    print("Input Scoresheet:")
    t2 = input()

    # Se manda la jugada:
    # '4'
    # '5
    # '6'
    # 'straight'
    # 'fullhouse'
    # 'four_of_a_kind'
    # 'yahtzee'
    print("Input Play:")
    t3 = '_' + input()

    # Se manda el multiplicador del score (Para _4, _5 y _6 se manda la cantidad de dados con dicho numero)
    # para el resto 1
    print("Input Multiplier:")
    t4 = input()

    # Se manda si se obtuvo la jugada en un turno (0 o 1)
    print("Input if it was a First Roll Play:")
    t5 = bool(input())

    message = {'player':t1, 'scoresheet':t2, 'play':t3, 'multiplier':t4, 'bonus':t5}
    print('Se envia: ')
    print(message)
    emit('update group', message)

#def player_move(player_name, move, score):
#    pass1
# Se define la funcion que envia los cambios a ser mostrados en la planilla de resultados
# Make this shiet


if __name__ == '__main__':
    socketio.run(app)


#@socketio.on('my_event')
# var['key']
# var.get('key', valor_por_default)
