from logic import Logic
from guardadosObj import guardadosObj


class guardadosLogic(Logic):
    def __init__(self):
        super().__init__()
        self.keys = [
            "id",
            "id_inversionista",
            "id_producto",
        ]

    def guardar(self, id_inversionista, id_producto):
        dataBase = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.guardado (id, id_inversionista, id_producto) "
            + "values (0, %s, %s);"
        )
        data = (id_inversionista, id_producto)
        rows = dataBase.executeNonQueryRowsTuple(sql, data)
        return rows

    def getAllGuardados(self, id_inversionista):
        dataBase = self.get_databaseXObj()
        sql = (
            "select productos.id, productos.descripcion, productos.nombre, productos.nombre_foto, emprendimiento.nombre, emprendimiento.id "
            + "from inversionista inner join guardado on guardado.id_inversionista = inversionista.id "
            + "inner join productos on productos.id = guardado.id_producto "
            + "inner join emprendimiento on productos.id_emprendimiento = emprendimiento.id "
            + f"where id_inversionista = {id_inversionista};"
        )
        data = dataBase.executeQuery(sql)
        return data

    def deleteGuardado(self, id_inversionista, id_producto):
        database = self.get_databaseXObj()
        sql = f"delete from fishingdb.guardado where guardado.id_inversionista = {id_inversionista} and guardado.id_producto = {id_producto};"
        rows = database.executeNonQueryRows(sql)
        return rows

    def checkGuardado(self, id_inversionista, id_producto):
        database = self.get_databaseXObj()
        sql = f"select * from fishingdb.guardado where guardado.id_inversionista = {id_inversionista} and guardado.id_producto = {id_producto};"
        print(sql)
        data = database.executeQuery(sql)
        counter = 0
        for item in data:
            counter += 1

        if counter > 0:
            return True
        else:
            return False
