from socketIO_client import SocketIO, LoggingNamespace

with SocketIO('localhost', 5001) as socketIO:
    message = {'data': 'Hi'}
    socketIO.emit('test', message)
    print('Done')
