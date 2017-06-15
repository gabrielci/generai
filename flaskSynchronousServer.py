from flask import Flask, render_template, request
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
def init():
    if request.method == 'POST':
        # Intialize match list and obtain the data send by client
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
                print match

        return 'A new match has begun'
    return 'Does not accept requests other than POST'

# Function to update the current scoreboard with what the game program tells it
@app.route('/updatematch', methods=['POST'])
def admin_stuff():
    if request.method == 'POST':
        global match

        # We save the data we got from the main program
        r = request.form
        print(r)

        # We get the corresponding fields (Done this way so its easier to read)
        pname = r.get('player', type=str)
        scnum = r.get('scoresheet_n', type=int)
        dec = r.get('decision', type=str)
        val = r.get('value', type=int)

        # We update the scoreboard with the data obtained
        match[scnum][pname].update({dec: val})

        return 'New match data has arrived'
    return 'Does not accept requests other than POST'

# We host the server on the localhost on a selected port
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
