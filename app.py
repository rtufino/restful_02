#!venv/bin/python
from flask import Flask
from flask_restful import Api
from servicios import ListaTareas, poblar_basedatos, TareaItem

app = Flask(__name__)
api = Api(app)

api.add_resource(ListaTareas, '/api/v2.0/tareas')
api.add_resource(TareaItem, '/api/v2.0/tareas/<int:tarea_id>')


@app.route('/')
def index() -> str:
    return "Hola mundo!"


@app.route('/poblar')
def poblar() -> str:
    poblar_basedatos()
    return "Datos poblados en la base"


if __name__ == '__main__':
    app.run(debug=True)
