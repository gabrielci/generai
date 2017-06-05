from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Testing
@socketio.on('got connected')
def sendDataIO():
    players_input = input("Ingrese datos: ")
    jsonstuff = {"var1":players_input, "var2":(players_input+1)}
    print('Se envia: ')
    print(players_input)
    print(players_input + 1)
    print jsonstuff
    print jsonstuff["var1"]
    print jsonstuff["var2"]
    emit('update group', jsonstuff)

#def player_move(player_name, move, score):
#    pass
# Se define la funcion que envia los cambios a ser mostrados en la planilla de resultados
# Make this shiet


if __name__ == '__main__':
    socketio.run(app)


#@socketio.on('my_event')
# var["key"]
# var.get("key", valor_por_default)
