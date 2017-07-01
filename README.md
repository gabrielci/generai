# generai

Framework para un concurso de programación basado en el juego de
GENERALA.

Herramientas Opcionales:
	Installar virtualenv y crear un virtual environment
		pip install virtualenv

		virtualenv -p /dir/a/ejecutable/de/python2.7/ejecutable nombre_del_virtualenv

	Utilizar un IDE como PyCharm que puede crear un virtual environment y tiene un menu para instalar librerias en el env


Requerimientos
	Python 2.7

	Libreria de python para levantar un servidor sincrono
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

Informacion y uso:
	Se deben correr tres procesos de python (Python 2.7):
		flaskSynchronousServer.py
			Es el servidor sincrono que se encarga de servir la pagina y comunicar el juego con el servidor asincrono

		flaskAsynchronousServer.py
			Es el servidor asincrono que se encarga de manejar las conexiones con los clientes via websocket y pasa
			la informacion que recibe del servidor sincrono a todos los clientes conectados

		generai.py
			Es el juego mismo, se maneja el juego mediante este proceso dejando crear una partida utilizando los
			plugins como jugadores y eligiendo la cantidad de partidas (O "scoresheets") que jugaran (Si se elige
			al jugador CONIO se estaria poniendo el input manual por este proceso)

	La pagina para visualizar se accede via el puerto 5000, por debajo el servidor asincrono utiliza el 5001, para su 
	propia pc puede acceder mediante "localhost:5000" de otra mediante "ip_address_del_server:5000"

	Una vez en la pagina siempre se reflejaran los datos de la partida en el tablero y menu, se puede entrar en el
	medio de una partida y apareceran los datos actuales en la tabla y continuara con las actualizaciones a medida que
	lleguen (Se usa un timer para que se actualize la tabla de puntajes lentamente que sino es instantaneo).

	Por ultimo si se empieza una partida nueva en el proceso "generai.py" instantaneamente se cargaran los datos y tablas
	de esta, inclusive si no se termino de desplegar la partida anterior.

	Des-comentar la linea "# app.config['DEBUG'] = True" al comienzo del codigo de cada servidor para motivos de prueba