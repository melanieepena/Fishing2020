from logic import Logic
import os


class busquedaLogic(Logic):
    def __init__(self):
        super().__init__()
        self.keys = []

    def buscarEmprendimiento(self, busqueda):
        dataBase = self.get_databaseXObj()
        sql = (
            "select id from fishingdb.emprendimiento "
            + f"where nombre LIKE '%{busqueda}%';"
        )
        data = dataBase.executeQuery(sql)
        lista = []
        for registro in data:
            currentList = list(registro)
            lista.append(currentList[0])
        return lista

    def buscarProducto(self, busqueda):
        dataBase = self.get_databaseXObj()
        sql = (
            "select emprendimiento.nombre, productos.descripcion, productos.nombre, productos.nombre_foto, emprendimiento.id ,productos.foto "
            + "from productos inner join emprendimiento on productos.id_emprendimiento = emprendimiento.id "
            + f"where productos.nombre LIKE '%{busqueda}%';"
        )
        data = dataBase.executeQuery(sql)
        return data
