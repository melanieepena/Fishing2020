from logic import Logic


class likeLogic(Logic):
    def __init__(self):
        super().__init__()
        self.keys = [
            "id",
            "id_inversionista",
            "id_producto",
        ]

    def like(self, id_inversionista, id_producto):
        dataBase = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.reaccion (id, id_inversionista, id_producto) "
            + "values (0, %s, %s);"
        )
        data = (id_inversionista, id_producto)
        rows = dataBase.executeNonQueryRowsTuple(sql, data)

        contador = self.getNumLikes(id_producto)
        sql2 = (
            "update fishingdb.productos"
            + f" set likes ={contador + 1}"
            + f" where id = {id_producto};"
        )
        rows = dataBase.executeNonQueryRows(sql2)
        return rows

    def getNumLikes(self, id_producto):
        dataBase = self.get_databaseXObj()
        sql = (
            "select productos.likes from fishingdb.productos "
            + f"where productos.id = {id_producto};"
        )
        data = dataBase.executeQuery(sql)
        return data[0][0]

    def unLike(self, id_inversionista, id_producto):
        dataBase = self.get_databaseXObj()
        sql = (
            "delete from fishingdb.reaccion "
            + f"where id_inversionista = {id_inversionista} and id_producto = {id_producto};"
        )
        rows = dataBase.executeNonQueryRows(sql)

        contador = self.getNumLikes(id_producto)
        sql2 = (
            "update fishingdb.productos"
            + f" set likes ={contador - 1}"
            + f" where id = {id_producto};"
        )
        rows = dataBase.executeNonQueryRows(sql2)
        return rows

    def getAllReaccionesByIdEmprendimiento(self, id_emprendimiento):
        dataBase = self.get_databaseXObj()
        sql = (
            "select reaccion.* from fishingdb.productos inner join fishingdb.reaccion "
            + "on productos.id = reaccion.id_producto "
            + f"where productos.id_emprendimiento = {id_emprendimiento};"
        )
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data
