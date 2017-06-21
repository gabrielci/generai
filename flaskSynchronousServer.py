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
        print('This is the following player numbering')
        print(player_numbering)

        # We append as many scoresheet libraries as "nscoresheets" says to the match list
        for i in range(0, num_scoresheets):
            match.append({})
            for j in player_list:
                match[i].update({j: {}})

        # Last we pass the initial data to the async server so it can tell the client
        message = {'player_amount': len(player_list), 'player_numbering': player_numbering, 'num_scoresheets': num_scoresheets}
        try:
            with SocketIO('localhost', 5001) as socketIO:
                socketIO.emit('init_match', message)
                print('Passed data to Async Server via websocket')
        except:
            print('Error - Failed to initialize - The server was not able to communicate with the asynchronous server!')

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
        p_name = r.get('p_name', type=str)

        for i in player_numbering:
            if player_numbering[i] == p_name:
                p_num = i
                break

        scoresheet_num = r.get('scoresheet_num', type=int)
        play = '_' + r.get('play', type=str)
        multiplier = r.get('multiplier', type=int)
        bonus = r.get('bonus', type=int)
        value = r.get('value', type=int)

        # We update the local scoreboard with the data obtained
        match[scoresheet_num][p_name].update({play: value})
        # We make the message to be sent
        message = {'p_num': p_num, 'scoresheet_num': scoresheet_num, 'play': play, 'multiplier': multiplier, 'bonus': bonus}
        print('We are trying to send (Sync -> Async):')
        print(message)
        # We send the Async Server the data so it can update the viewers
        try:
            with SocketIO('localhost', 5001) as socketIO:
                socketIO.emit('update_match', message)
                print('Passed data to Async Server via websocket')
        except:
            print('Error - Failed to update - The server was not able to communicate with the asynchronous server!')

        return 'New match data has arrived'
    return 'Does not accept requests other than POST'

# We host the server on the localhost on a selected port
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    print "asd"
