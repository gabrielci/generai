import random

av_plays = ['_4', '_5', '_6', '_straight', '_fullhouse', '_four_of_a_kind', '_yahtzee']
for player_turn in range(0,3):
    for scoresh in range(0, 3):
        for play in av_plays:
            if play == '_4' or play == '_5' or play == '_6':
                mult = random.randint(0, 5)
                message = {'player': player_turn, 'scoresheet': scoresh, 'play': play, 'multiplier': mult, 'bonus': 0}
            else:
                bon = random.randint(0, 1)
                message = {'player': player_turn, 'scoresheet': scoresh, 'play': play, 'multiplier': 1, 'bonus': bon}

            print message




