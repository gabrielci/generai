from flask import Flask, render_template

# Se crea el objeto Flask del servidor sincrono
app = Flask(__name__)
# Activamos el Debug mode (Se comenta esta linea cuando se hace el servidor real)
app.config['DEBUG'] = True


@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('alseis.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
