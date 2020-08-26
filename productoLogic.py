from logic import Logic
from productoObj import productoObj
import os


class productoLogic(Logic):
    def __init__(self):
        super().__init__()
        self.keys = [
            "id",
            "nombre",
            "nombre_foto",
            "foto",
            "descripcion",
            "costo_unitario",
            "precio_venta",
            "patente",
            "id_emprendimiento",
            "likes",
        ]

    def insertNewProducto(
        self,
        name,
        foto,
        descripcion,
        costo_unitario,
        precio_venta,
        patente,
        id_emprendimiento,
    ):
        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.productos (id, nombre, descripcion, costo_unitario, precio_venta, patente, id_emprendimiento) "
            + "values (0, %s, %s, %s, %s, %s, %s);"
        )
        data = (
            name,
            descripcion,
            costo_unitario,
            precio_venta,
            patente,
            id_emprendimiento,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)

        id_producto = self.getIdProductoByIdEmprendimiento(
            id_emprendimiento, descripcion
        )
        nombre_foto = str(id_producto) + ".png"

        sql2 = (
            "update fishingdb.productos "
            + "set productos.nombre_foto = %s, productos.foto = %s "
            + "where productos.id = %s;"
        )
        data2 = (nombre_foto, foto, id_producto)
        database.executeNonQueryRowsTuple(sql2, data2)
        self.saveImagesProductos(id_producto)

        return rows

    def insertNewProductoWithoutPhoto(
        self,
        name,
        nombre_foto,
        descripcion,
        costo_unitario,
        precio_venta,
        patente,
        id_emprendimiento,
    ):
        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.productos (id, nombre, nombre_foto, descripcion, costo_unitario, precio_venta, patente, id_emprendimiento) "
            + "values (0, %s, %s, %s, %s, %s, %s, %s);"
        )
        data = (
            name,
            nombre_foto,
            descripcion,
            costo_unitario,
            precio_venta,
            patente,
            id_emprendimiento,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)
        return rows

    def getAllProductosByIdEmprendimiento(self, id_emprendimiento):
        dataBase = self.get_databaseXObj()
        sql = f"select * from fishingdb.productos where id_emprendimiento = {id_emprendimiento};"
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data

    def saveImagesProductos(self, id_producto):
        data = self.getProductoByIdDiccionary(id_producto)
        for registro in data:
            foto = registro["foto"]
            nombre_foto = registro["nombre_foto"]
            if nombre_foto != "products.png":
                path = os.getcwd() + "\\static\\images\\productos\\" + nombre_foto
                with open(path, "wb") as file:
                    file.write(foto)

    def deleteProducto(self, id_producto):
        database = self.get_databaseXObj()
        sql = "delete from fishingdb.productos " + f"where id = {id_producto};"
        rows = database.executeNonQueryRows(sql)
        return rows

    def updateProductoWithoutPhoto(
        self, id_producto, name, descripcion, costo_unitario, precio_venta, patente,
    ):
        database = self.get_databaseXObj()
        sql = (
            "update fishingdb.productos"
            + f" set nombre ='{name}', descripcion='{descripcion}', costo_unitario={costo_unitario}, precio_venta={precio_venta}, patente={patente}"
            + f" where id = {id_producto};"
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def updateProducto(
        self,
        id_producto,
        name,
        foto,
        descripcion,
        costo_unitario,
        precio_venta,
        patente,
    ):
        database = self.get_databaseXObj()
        sql = (
            "update fishingdb.productos"
            + " set nombre = %s, foto = %s, descripcion = %s, costo_unitario = %s, precio_venta = %s, patente = %s, nombre_foto = %s"
            + " where id = %s;"
        )
        data = (
            name,
            foto,
            descripcion,
            costo_unitario,
            precio_venta,
            patente,
            str(id_producto) + ".png",
            id_producto,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)
        self.saveImagesProductos(id_producto)
        return rows

    def getProductoById(self, id):
        dataBase = self.get_databaseXObj()
        sql = "SELECT * FROM fishingdb.productos " + f"where productos.id = {id};"
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            prodObj = productoObj(
                data_dic["id"],
                data_dic["nombre"],
                data_dic["nombre_foto"],
                data_dic["foto"],
                data_dic["descripcion"],
                data_dic["costo_unitario"],
                data_dic["precio_venta"],
                data_dic["patente"],
                data_dic["id_emprendimiento"],
            )
            return prodObj
        else:
            return None

    def getIdProductoByIdEmprendimiento(self, id_emprendimiento, descripcion):
        dataBase = self.get_databaseXObj()
        sql = (
            "SELECT productos.id FROM fishingdb.productos "
            + f"where productos.id_emprendimiento = {id_emprendimiento} and productos.descripcion = '{descripcion}';"
        )
        data = dataBase.executeQuery(sql)
        id_producto = data[0][0]
        return id_producto

    def getProductoByIdDiccionary(self, id):
        dataBase = self.get_databaseXObj()
        sql = "SELECT * FROM fishingdb.productos " + f"where productos.id = {id};"
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data
