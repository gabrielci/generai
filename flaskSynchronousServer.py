from flask import Flask, render_template, request
from socketIO_client import SocketIO
# We make the sync server flask object
app = Flask(__name__)
# Debug mode (Uncomment for testing purposes)
app.config['DEBUG'] = True

# Init
match = []

# Scoreboard Page
@app.route('/')
def index():
    return render_template('alseis.html')


# Funtion that gets a copy of the initial state of the game (It gets number of scoresheets as well as the player names)
# The game itself checks for no duplicate names and such, this is only run when its ready to start the actual game on
# the game program
@app.route('/initmatch', methods=['POST'])
def init_match():
    if request.method == 'POST':
        # Intialize match list and obtain the data sent by client
        global match
        match = []
        r = request.form

        # We get the number of scoresheets for our loop upper limit
        nscoresheets = r.get('nscoresheets', type=int)

        # We get the players so we can build the scoreboard
        seq = r.getlist('players', type=str)

        # We append as many scoresheet libraries as "nscoresheets" says to the match list
        for i in range(0, nscoresheets):
            match.append({})
            for j in seq:
                match[i].update({j: {}})

        print("Initial match status")
        print(match)
        return 'A new match has begun'
    return 'Does not accept requests other than POST'


# Function to update the current scoreboard with what the game program tells it
@app.route('/updatematch', methods=['POST'])
def update_match():
    if request.method == 'POST':
        global match

        # We save the data we got from the main program
        r = request.form

        # We get the corresponding fields (Done this way so its easier to read)
        pname = r.get('player', type=str)
        scnum = r.get('scoresheet_n', type=int)
        play = r.get('play', type=str)
        bonus = int(r.get('bonus', type=bool))
        val = r.get('value', type=int)

        # We calculate the base value multiplier we need to send to the client
        # If we chose '4' and scored  20 it means we have a multiplier of 5, 4*5 = 20
        # For the more difficult plays you either have the play or dont so the mult is 0 or 1
        if play == '4':
            mult = val/4
        elif play == '5':
            mult = val / 5
        elif play == '6':
            mult = val / 6
        else:
            if val != 0:
                mult = 1
            else:
                mult = 0

        # We make the message to be sent
        message = {'player': pname, 'scoresheet': scnum, 'play': play, 'multiplier': mult, 'bonus': bonus*mult}

        # We update the local scoreboard with the data obtained
        match[scnum][pname].update({play: val})

        # We send the Async Server the data so it can update the viewers
        with SocketIO('localhost', 5001) as socketIO:
            socketIO.emit('update_state', message)
            print('Passed data to Async Server via websocket')

        return 'New match data has arrived'
    return 'Does not accept requests other than POST'

# We host the server on the localhost on a selected port
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    print "asd"
