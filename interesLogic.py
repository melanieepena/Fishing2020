from logic import Logic
from especialidadObj import especialidadObj


class interesLogic(Logic):
    def __init__(self):
        super().__init__()
        self.keys = [
            "id",
            "id_emprendimiento",
            "id_categoria",
        ]

    def getAllInteresByIdInv(self, id_inv):
        dataBase = self.get_databaseXObj()
        sql = (
            "select emprendimiento.descripcion, emprendimiento.nombre, emprendimiento.nombre_foto, emprendimiento.id "
            + "from inversionista inner join interes on interes.id_inversionista = inversionista.id "
            + "inner join categoria on categoria.id = interes.id_categoria "
            + "inner join especialidad on especialidad.id_categoria = categoria.id "
            + "inner join emprendimiento on emprendimiento.id = especialidad.id_emprendimiento "
            + f"where inversionista.id = {id_inv};"
        )
        data = dataBase.executeQuery(sql)
        return data
