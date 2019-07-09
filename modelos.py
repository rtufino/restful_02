from pony import orm

db = orm.Database()


class Tarea(db.Entity):
    _table_ = 'Tarea'

    titulo = orm.Required(str)
    descripcion = orm.Required(str)
    hecho = orm.Required(bool)

    def __str__(self):
        return self.titulo
