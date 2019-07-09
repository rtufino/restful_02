from flask_restful import Resource, abort, request
from modelos import *

db.bind('sqlite', 'tareas.db', create_db=True)
db.generate_mapping(create_tables=True)


def poblar_basedatos():
    with orm.db_session:
        t1 = Tarea(
            titulo='Enseñar Flask Restful',
            descripcion='Hacer un ejemplo básico con Flask y RESTful.',
            hecho=False
        )
        t2 = Tarea(
            titulo='Aprender Docker',
            descripcion='Entender la tecnología y estudiar un ejemplo.',
            hecho=False
        )
        t3 = Tarea(
            titulo='Aprender Google Cloud',
            descripcion='Crear una cuenta en GCP y empezar hacer pruebas.',
            hecho=False
        )


class ListaTareas(Resource):
    def get(self):
        # $ curl -i -X GET http://localhost:5000/api/v2.0/tareas
        with orm.db_session:
            return {
                       item.id: {
                           'titulo': item.titulo,
                           'descripcion': item.descripcion,
                           'hecho': item.hecho
                       }
                       for item in Tarea.select()
                   }, 200

    def post(self):
        # $ curl -i -H "Content-Type: application/json" -X POST -d '{"titulo":"Investigar SOAP","descripcion":"Buscar
        # información sobre esta tecnología"}' http://localhost:5000/api/v2.0/tareas
        if not request.is_json:
            abort(404, message="La petición no se encuentra en formato application/json")

        with orm.db_session:
            item = Tarea(
                titulo=request.json['titulo'],
                descripcion=request.json['descripcion'],
                hecho=False
            )

        return {"tarea": item.to_dict()}, 201


class TareaItem(Resource):
    def get(self, tarea_id):
        # $ curl -i -X GET http://localhost:5000/api/v2.0/tareas/2
        try:
            with orm.db_session:
                tarea = Tarea[tarea_id]
                return {"tarea": tarea.to_dict()}, 200
        except orm.ObjectNotFound:
            abort(404, message="Tarea con id={} no existe".format(tarea_id))

    def put(self, tarea_id):
        # $ curl -i -H "Content-Type: application/json" -X PUT -d '{"titulo":"Desaprender SOAP","descripcion":"Olvidar
        # lo que sabemos de SOAP","hecho":true}' http://localhost:5000/api/v2.0/tareas/4
        if not request.is_json:
            abort(404, message="La petición no se encuentra en formato application/json")
        try:
            with orm.db_session:
                tarea = Tarea[tarea_id]
                tarea.titulo = request.json['titulo']
                tarea.descripcion = request.json['descripcion']
                tarea.hecho = request.json['hecho']
                return {"tarea": tarea.to_dict()}, 200
        except orm.ObjectNotFound:
            abort(404, message="Tarea con id={} no existe".format(tarea_id))

    def delete(self, tarea_id):
        # $ curl -i -X DELETE http://localhost:5000/api/v2.0/tareas/4
        try:
            with orm.db_session:
                tarea = Tarea[tarea_id]
                if tarea:
                    tarea.delete()
        except orm.ObjectNotFound:
            abort(404, message="Tarea con id={} no existe".format(tarea_id))
        return {'message': 'Tarea eliminada exitosamente'}, 200
