from logic import Logic
from emprendedorObj import emprendedorObj
import os


class emprendedorLogic(Logic):
    def __init__(self):
        super().__init__()
        self.keys = [
            "id",
            "nombre",
            "email",
            "telefono",
            "nombre_foto",
            "foto",
            "id_usuario",
            "pais",
            "ciudad",
            "biografia",
        ]

    # Insertar emprendimiento
    def insertNewEmprendedor(
        self, name, email, phone, id_user, country, city, biografia, foto
    ):
        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.emprendedor (id, nombre, email, telefono, id_usuario, pais, ciudad, biografia) "
            + "values (0, %s, %s, %s, %s, %s, %s, %s);"
        )
        data = (
            name,
            email,
            phone,
            id_user,
            country,
            city,
            biografia,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)

        id_emprendedor = self.getIdEmprendedorByIdUsuario(id_user)
        nombre_foto = str(id_emprendedor) + ".png"

        sql2 = (
            "update fishingdb.emprendedor "
            + "set emprendedor.nombre_foto = %s, emprendedor.foto = %s "
            + "where emprendedor.id = %s;"
        )
        data2 = (nombre_foto, foto, id_emprendedor)
        database.executeNonQueryRowsTuple(sql2, data2)

        self.saveImagesEmprendedor(id_user)

        return rows

    def insertNewEmprendedorWithoutPhoto(
        self, name, email, phone, id_user, country, city, biografia, nombre_foto
    ):
        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.emprendedor (id, nombre, email, telefono, id_usuario, pais, ciudad, biografia, nombre_foto) "
            + "values (0, %s, %s, %s, %s, %s, %s, %s, %s);"
        )
        data = (
            name,
            email,
            phone,
            id_user,
            country,
            city,
            biografia,
            nombre_foto,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)
        return rows

    def getNewEmprendedor(
        self, name, email, phone, id_user, country, city,
    ):
        dataBase = self.get_databaseXObj()
        sql = "select * from fishingdb.emprendedor " + f"where id_usuario = {id_user};"
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            empObj = emprendedorObj(
                data_dic["id"],
                data_dic["nombre"],
                data_dic["email"],
                data_dic["telefono"],
                data_dic["id_usuario"],
                data_dic["pais"],
                data_dic["ciudad"],
                data_dic["biografia"],
                data_dic["foto"],
                data_dic["nombre_foto"],
            )
            return empObj
        else:
            return None

    def getEmprendedorByUser(self, id_user):
        dataBase = self.get_databaseXObj()
        sql = "select * from fishingdb.emprendedor " + f"where id_usuario = {id_user};"
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            empObj = emprendedorObj(
                data_dic["id"],
                data_dic["nombre"],
                data_dic["email"],
                data_dic["telefono"],
                data_dic["id_usuario"],
                data_dic["pais"],
                data_dic["ciudad"],
                data_dic["biografia"],
                data_dic["foto"],
                data_dic["nombre_foto"],
            )
            return empObj
        else:
            return None

    # Update
    def updateEmprendedorbyIdUsuario(
        self, id, nombre, email, telefono, pais, ciudad, biografia
    ):
        database = self.get_databaseXObj()
        sql = (
            "update fishingdb.emprendedor "
            + f"set emprendedor.nombre = '{nombre}', emprendedor.email = '{email}', emprendedor.telefono = '{telefono}',  "
            + f"emprendedor.pais = '{pais}', emprendedor.ciudad = '{ciudad}', emprendedor.biografia = '{biografia}' "
            + f"where emprendedor.id_usuario = '{id}';"
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def updateEmprendedorbyIdUsuarioWithPhoto(
        self, id, nombre, email, telefono, pais, ciudad, biografia, foto
    ):
        database = self.get_databaseXObj()
        nombre_foto = str(self.getIdEmprendedorByIdUsuario(id)) + ".png"
        sql = (
            "update fishingdb.emprendedor "
            + "set emprendedor.nombre = %s, emprendedor.email = %s, emprendedor.telefono = %s, "
            + "emprendedor.pais = %s, emprendedor.ciudad = %s, emprendedor.biografia = %s, "
            + "emprendedor.nombre_foto = %s, emprendedor.foto = %s "
            + "where emprendedor.id_usuario = %s;"
        )
        data = (nombre, email, telefono, pais, ciudad, biografia, nombre_foto, foto, id)
        rows = database.executeNonQueryRowsTuple(sql, data)
        self.saveImagesEmprendedor(id)
        return rows

    # Obtener datos byId
    def getDatosGeneralesById(self, idUsuario):
        dataBase = self.get_databaseXObj()

        sql = (
            "select * from fishingdb.emprendedor inner join fishingdb.usuario "
            + "on emprendedor.id_usuario = usuario.id "
            + f"where usuario.id like '{idUsuario}';"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data

    # Imagen
    def saveImagesEmprendedor(self, idUsuario):
        data = self.getDatosGeneralesById(idUsuario)
        for registro in data:
            foto = registro["foto"]
            nombre_foto = registro["nombre_foto"]
            if nombre_foto != "default.png":
                path = os.getcwd() + "\\static\\images\\emprendedor\\" + nombre_foto
                with open(path, "wb") as file:
                    file.write(foto)

    def getIdEmprendedorByIdUsuario(self, id_usuario):
        dataBase = self.get_databaseXObj()
        sql = (
            "select emprendedor.id from fishingdb.emprendedor inner join fishingdb.usuario "
            + "on emprendedor.id_usuario = usuario.id "
            + f"where usuario.id like '{id_usuario}';"
        )
        data = dataBase.executeQuery(sql)
        id_emprendedor = data[0][0]
        return id_emprendedor

    def getNotification(self, idUsuario):
        database = self.get_databaseXObj()
        sql = (
            f"select notificaciones.mensaje, notificaciones.fecha, notificaciones.hora from fishingdb.notificaciones where id_emprendedor={idUsuario} "
            + "Order by notificaciones.fecha desc, notificaciones.hora desc limit 5;"
        )
        print(sql)
        data = database.executeQuery(sql)
        data = self.tupleToDictionaryList(data, ["mensaje", "fecha", "hora"],)
        return data

    def getAllEmprendedores(self):
        dataBase = self.get_databaseXObj()
        sql = "select * from fishingdb.emprendedor;"
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data

    def deleteEmprendedor(self, id):
        database = self.get_databaseXObj()
        sql = f"delete from fishingdb.emprendedor where emprendedor.id = '{id}';"
        rows = database.executeNonQueryRows(sql)
        return rows
