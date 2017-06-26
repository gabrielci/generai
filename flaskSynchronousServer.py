from flask import Flask, render_template, request
from socketIO_client import SocketIO
# We make the sync server flask object
app = Flask(__name__)
# Debug mode (Uncomment for testing purposes)
app.config['DEBUG'] = True

# Initialize match and PlayerName: PlayerNumber containers
match = []
player_numbering = {}


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
        global player_numbering
        match = []
        player_numbering = {}

        r = request.form

        # We get the number of scoresheets of the new match
        num_scoresheets = r.get('num_scoresheets', type=int)
        # We get the player name list
        player_list = r.getlist('players', type=str)

        # We assign a number to each player (Based on order in dictionary)
        for i in range(0, len(player_list)):
            player_numbering[str(i)] = player_list[i]

        # We append as many scoresheet libraries as "nscoresheets" says to the match list
        for i in range(0, num_scoresheets):
            match.append({})
            for j in player_list:
                match[i].update({j: {}})

        # Last we pass the initial data to the async server so it can tell the client
        message = {'player_amount': len(player_list), 'player_numbering': player_numbering, 'num_scoresheets': num_scoresheets}
        print('We are trying to send init message (Sync Server -> Async Server):')
        print(message)
        try:
            with SocketIO('localhost', 5001) as socketIO:
                socketIO.emit('init_match', message)
        except:
            print('Error - Failed to initialize - The server was not able to communicate with the asynchronous server!')

        return 'A new match has begun'
    return 'Does not accept requests other than POST'


# Function to update the current scoreboard with what the game program tells it
@app.route('/updatematch', methods=['POST'])
def update_match():
    if request.method == 'POST':
        global match

        # We save the data we got from the main program
        r = request.form

        # We check for the 'game has finished' flag first
        if int(r['game_has_ended']):
            # We make the message to be sent and try to send it to the Async Server
            message = {'game_has_ended': 1}
            print('We are trying to send game has ended message (Sync Server -> Async Server):')
            print(message)

            try:
                with SocketIO('localhost', 5001) as socketIO:
                    socketIO.emit('update_match', message)
            except:
                print('Error - Failed to update - The server was not able to communicate with the asynchronous server!')

        else:
            # We get the corresponding fields (Shown this way so its easier to read)
            print("Got em")
            p_name = r['p_name']


            for i in player_numbering:
                if player_numbering[i] == p_name:
                    p_num = i
                    break

            scoresheet_num = int(r['scoresheet_num'])
            play = '_' + r['play']
            multiplier = int(r['multiplier'])
            bonus = int(r['bonus'])
            value = int(r['value'])

            # We update the local scoreboard with the data obtained
            match[scoresheet_num][p_name].update({play: value})

            # We make the message to be sent and try to send it to the Async Server
            message = {'p_num': p_num, 'scoresheet_num': scoresheet_num, 'play': play, 'multiplier': multiplier, 'bonus': bonus, 'game_has_ended': 0}
            print('We are trying to send update message (Sync Server -> Async Server):')
            print(message)

            try:
                with SocketIO('localhost', 5001) as socketIO:
                    socketIO.emit('update_match', message)
            except:
                print('Error - Failed to update - The server was not able to communicate with the asynchronous server!')

        return 'New match data has arrived'
    return 'Does not accept requests other than POST'

# We host the server on the localhost on a selected port
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
