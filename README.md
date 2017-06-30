# generai

Framework para un concurso de programación basado en el juego de
GENERALA.

Opcional:
	Installar virtualenv y crear un virtual environment
		pip install virtualenv

		virtualenv -p /dir/a/ejecutable/de/python2.7/ejecutable nombre_del_virtualenv

	Utilizar un IDE como PyCharm


Requerimientos
	Python 2.7

	Libreria de python para levatar un servidor sincrono
	http://flask.pocoo.org/
	pip install flask

	Libreria de python para un servidor asincrono que utiliza el protocolo socketIO
	https://flask-socketio.readthedocs.io/en/latest/
	pip install flask-socketio

	Manejador de web sockets 
	pip install eventlet

	Libreria para poder acceder a la informacion de un request del tipo "POST" en un servidor http
	pip install requests

	Libreria de Python para hacer un cliente en python que se comunique mediante el protocolo socketIO
	https://pypi.python.org/pypi/socketIO-client
	pip install socketIO-client

Informacion:
	La pagina se accede via el puerto 5000, por debajo el servidor asincrono utiliza el 5001, para su 
	propia pc puede acceder mediante "localhost:5000" sino mediante "ip_address:5000"