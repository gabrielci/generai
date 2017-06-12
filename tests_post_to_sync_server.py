import requests

while(1):
    print("Input Player:")
    t1 = input()

    message = {'player':t1, 'scoresheet': 0, 'play': '_6', 'multiplier': 4, 'bonus': 0}
    print('Se envia: ')
    print(message)

    r = requests.get('http://127.0.0.1:5001/admin', data = message)