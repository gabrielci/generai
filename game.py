# To talk to the Sync server
import requests

#
import sys
import traceback

from helper import print_scoresheets

from generala import get_random_dice, valid_play, play_value

class Player():#segundo comentario de prueba

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def game_start(self, nplayers):
        pass

    def play(self, dice, players, scoresheets):
        pass

    def notify(self, not_type, message):
        pass

class Game():

    def __init__(self, nscoresheets):
        self.nscoresheets = nscoresheets
        self.nplayers = 0
        self.players_plugins = {}
        self.players = []
        self.scoresheets = []
        for i in range(nscoresheets):
            self.scoresheets.append({})

    def add_player(self, player):
        name = player.name()
        self.players_plugins[name] = player
        self.players.append(name)
        for i in range(self.nscoresheets):
            self.scoresheets[i][name] = {}
        self.nplayers = self.nplayers + 1

    def start(self):
        # plays are:
        # 4
        # 5
        # 6
        # ESCALERA
        # FULL
        # POKER
        # GENERALA

        # We send the initial data (Players names and number of scoresheets) to the sync server
        message = {'players': self.players, "num_scoresheets": self.nscoresheets}
        try:
            requests.post('http://127.0.0.1:5000/initmatch', data=message)
        except:
            print('Error - Failed to initialize - The game was not able to communicate with the synchronous server!')

        rounds = self.nscoresheets * 7
        for i in range(rounds):
            for player in self.players:
                self.turn(player)

        # We tell the sync server that the current match has finished
        message = {'game_has_ended': 1}
        print('We are trying to send the game has ended message (Game -> Sync Server):')
        print(message)
        try:
            requests.post('http://127.0.0.1:5000/updatematch', data=message)
        except:
            print('Error - Failed to update - The game was not able to communicate with the synchronous server!')


    def results(self):
        print_scoresheets(self.scoresheets)

    def turn(self, player):
        plugin = self.players_plugins[player]
        r = get_random_dice(5)
        nroll = 5

        for i in range(3):
            try:
                bonus = (nroll == 5)
                roll, decision, scoresheet = plugin.play(i, r, bonus, self.players, self.scoresheets)
                decision = decision.upper() if decision else None
                nroll = len(roll)
                if nroll > 0:
                    r0 = get_random_dice(nroll)
                    i = 0
                    for new_r in roll:
                        r[new_r] = r0[i]
                        i = i+1
                else:
                    if not valid_play(decision):
                        raise Exception('Play [{0}] is invalid'.format(decision))

                    # We keep the value for later use
                    scoresheet_num = scoresheet

                    scoresheet = self.scoresheets[scoresheet][player]

                    if decision not in scoresheet:
                        scoresheet[decision] = play_value(decision, r, bonus)

                        # We assign the corresponding values to the variables that will be sent
                        if decision == '4':
                            bonus = 0
                            play = decision
                            multiplier = scoresheet[decision] / 4
                        elif decision == '5':
                            bonus = 0
                            play = decision
                            multiplier = scoresheet[decision] / 5
                        elif decision == '6':
                            bonus = 0
                            play = decision
                            multiplier = scoresheet[decision] / 6
                        else:
                            if scoresheet[decision] != 0:
                                multiplier = 1
                            else:
                                multiplier = 0

                            bonus = int(bonus)*multiplier
                            # We translate the play input to the corresponding value in the server
                            if decision == 'ESCALERA':
                                play = 'straight'
                            elif decision == 'FULLHOUSE':
                                play = 'fullhouse'
                            elif decision == 'POKER':
                                play = 'four_of_a_kind'
                            else:  # decision == 'GENERALA'
                                play = 'yahtzee'
                        # We use a flag to tell the others when the game has finished, that way the client can turn off
                        # its timed function to display results (No point in keeping it checking for stuff that wont
                        # arrive)
                        game_has_ended = 0

                        # We make the message to be sent and try to tell it to the sync server
                        message = {'p_name': player, 'scoresheet_num': scoresheet_num, 'play': play, 'multiplier': multiplier, 'bonus': bonus, 'value': scoresheet[decision], 'game_has_ended': game_has_ended}
                        print('We are trying to send update message (Game -> Sync Server):')
                        print message
                        try:
                            requests.post('http://127.0.0.1:5000/updatematch', data=message)
                            print('Message sent')
                        except:
                            print('Error - Failed to update - The game was not able to communicate with the synchronous server!')

                    else:
                        raise Exception('Decision [{0}] is already taken'.format(decision))
                    break

            except Exception as e:
                print(traceback.format_exc())
                print("Error inesperadamente inesperado: {0}".format(e))
                # NOTIFY

