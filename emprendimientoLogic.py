from logic import Logic
from emprendimientoObj import emprendimientoObj
from userLogic import UserLogic
from emprendedorLogic import emprendedorLogic
from inversorLogic import inversorLogic
from emprendedorObj import emprendedorObj
import os


class emprendimientoLogic(Logic):
    def __init__(self):
        super().__init__()
        self.keys = [
            "id",
            "estado",
            "descripcion",
            "historia",
            "eslogan",
            "inversion_inicial",
            "fecha_fundacion",
            "venta_año_anterior",
            "nombre",
            "nombre_foto",
            "foto",
            "video",
            "email",
            "telefono",
            "facebook",
            "instagram",
            "youtube",
        ]

    # Insert
    def insertNewEmprendimiento(
        self,
        estado,
        descripcion,
        historia,
        eslogan,
        inversion_inicial,
        fecha_fundacion,
        venta_año_anterior,
        id_emprendedor,
        nombre,
        foto,
        video,
        email,
        telefono,
        facebook,
        instagram,
        youtube,
    ):
        database = self.get_databaseXObj()
        sql = (
            "INSERT INTO fishingdb.emprendimiento (id, estado, descripcion, historia, eslogan, inversion_inicial, fecha_fundacion, venta_anio_anterior, "
            + "nombre, video, email, telefono, facebook, instagram, youtube) "
            + "VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        )

        data = (
            estado,
            descripcion,
            historia,
            eslogan,
            inversion_inicial,
            fecha_fundacion,
            venta_año_anterior,
            nombre,
            video,
            email,
            telefono,
            facebook,
            instagram,
            youtube,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)

        sql2 = (
            f"select emprendimiento.id from fishingdb.emprendimiento "
            + f"where emprendimiento.nombre = '{nombre}' and emprendimiento.eslogan = '{eslogan}' and emprendimiento.fecha_fundacion = '{fecha_fundacion}'"
        )
        data = database.executeQuery(sql2)
        id_emprendedimiento = data[0][0]
        self.insertFundadorById(id_emprendedor, id_emprendedimiento)

        sql3 = (
            "update fishingdb.emprendimiento "
            + "set emprendimiento.nombre_foto = %s, emprendimiento.foto = %s "
            + "where emprendimiento.id = %s;"
        )
        nombre_foto = str(id_emprendedimiento) + ".png"
        data2 = (nombre_foto, foto, id_emprendedimiento)
        database.executeNonQueryRowsTuple(sql3, data2)

        self.saveImagesEmprendimiento(id_emprendedimiento)

        return rows

    # Intert with out foto
    def insertNewEmprendimientoWithoutPhoto(
        self,
        estado,
        descripcion,
        historia,
        eslogan,
        inversion_inicial,
        fecha_fundacion,
        venta_año_anterior,
        id_emprendedor,
        nombre,
        nombre_foto,
        video,
        email,
        telefono,
        facebook,
        instagram,
        youtube,
    ):
        database = self.get_databaseXObj()
        sql = (
            "INSERT INTO fishingdb.emprendimiento (id, estado, descripcion, historia, eslogan, inversion_inicial, fecha_fundacion, venta_anio_anterior, "
            + "nombre, video, email, telefono, facebook, instagram, youtube, nombre_foto) "
            + "VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        )

        data = (
            estado,
            descripcion,
            historia,
            eslogan,
            inversion_inicial,
            fecha_fundacion,
            venta_año_anterior,
            nombre,
            video,
            email,
            telefono,
            facebook,
            instagram,
            youtube,
            nombre_foto,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)

        sql2 = (
            f"select emprendimiento.id from fishingdb.emprendimiento "
            + f"where emprendimiento.nombre = '{nombre}' and emprendimiento.eslogan = '{eslogan}' and emprendimiento.fecha_fundacion = '{fecha_fundacion}'"
        )
        data = database.executeQuery(sql2)
        id_emprendedimiento = data[0][0]
        self.insertFundadorById(id_emprendedor, id_emprendedimiento)

        return rows

    def getAllEmprendimientoLen(self):
        dataBase = self.get_databaseXObj()
        sql = "SELECT * FROM fishingdb.emprendimiento;"
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data

    def getEmprendimientoById(self, id):
        dataBase = self.get_databaseXObj()
        sql = (
            "SELECT * FROM fishingdb.emprendimiento "
            + f"where emprendimiento.id = {id};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            emprendimientObj = emprendimientoObj(
                data_dic["id"],
                data_dic["estado"],
                data_dic["descripcion"],
                data_dic["historia"],
                data_dic["eslogan"],
                data_dic["inversion_inicial"],
                data_dic["fecha_fundacion"],
                data_dic["venta_año_anterior"],
                data_dic["nombre"],
                data_dic["nombre_foto"],
                data_dic["foto"],
                data_dic["video"],
                data_dic["email"],
                data_dic["telefono"],
                data_dic["facebook"],
                data_dic["instagram"],
                data_dic["youtube"],
            )
            return emprendimientObj
        else:
            return None

    # QUIENES SOMOSSSS
    def getAllFundadores(self, idEmprendimiento):
        dataBase = self.get_databaseXObj()
        sql = (
            "select fishingdb.fundador.id, fishingdb.emprendedor.nombre_foto, fishingdb.emprendedor.foto, fishingdb.emprendedor.nombre, fishingdb.emprendedor.biografia, "
            + "fishingdb.fundador.id_emprendedor "
            + "from fishingdb.fundador "
            + "inner join fishingdb.emprendedor  on fishingdb.fundador.id_emprendedor = fishingdb.emprendedor.id "
            + "inner join fishingdb.emprendimiento on fishingdb.fundador.id_emprendimiento = fishingdb.emprendimiento.id "
            + f"where fishingdb.emprendimiento.id = {idEmprendimiento};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(
            data, ["id", "nombre_foto", "foto", "nombre", "biografia", "id_emprendedor"]
        )
        return data

    def checkUserAlredyExist(self, user, idEmprendimiento):
        id_usuario = UserLogic()
        usuario = id_usuario.getUserByUser(user)

        infoEmprendedor = emprendedorLogic()
        id_emprendedor = infoEmprendedor.getEmprendedorByUser(usuario.getId())
        dataBase = self.get_databaseXObj()
        sql = (
            "SELECT fundador.id FROM fishingdb.fundador "
            + f"where fundador.id_emprendedor = {id_emprendedor.getId()} and fundador.id_emprendimiento = {idEmprendimiento};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        counter = 0
        for item in data:
            counter += 1

        if counter > 0:
            return True
        else:
            return False

    def saveImagesFundadores(self, idEmprendimiento):
        data = self.getAllFundadores(idEmprendimiento)
        for registro in data:
            foto = registro["foto"]
            nombre_foto = registro["nombre_foto"]
            if nombre_foto != "default.png":
                path = os.getcwd() + "\\static\\images\\emprendedor\\" + nombre_foto
                with open(path, "wb") as file:
                    file.write(foto)

    def insertNewFundador(self, user, idEmprendimiento):

        id_usuario = UserLogic()
        usuario = id_usuario.getUserByUser(user)

        infoEmprendedor = emprendedorLogic()
        id_emprendedor = infoEmprendedor.getEmprendedorByUser(usuario.getId())

        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.fundador (id, id_emprendedor, id_emprendimiento) "
            + f"values (0, {id_emprendedor.getId()}, {idEmprendimiento});"
        )
        print(sql)
        rows = database.executeNonQueryRows(sql)
        return rows

    def insertNotificationFundador(self, user, id_emprendimiento):
        id_usuario = UserLogic()
        usuario = id_usuario.getUserByUser(user)
        Emprendedor = emprendedorLogic()
        Emprendimiento = emprendimientoLogic()
        id_emprendedor = Emprendedor.getEmprendedorByUser(usuario.getId())
        id_emprendimiento = Emprendimiento.getEmprendimientoById(id_emprendimiento)
        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.notificaciones (idnotificaciones, mensaje, id_emprendedor, fecha, hora) "
            + f"values (0, 'Te han añadido al emprendimiento: {id_emprendimiento.getNombre()}', {id_emprendedor.getId()}, current_date(), current_time());"
        )
        print(sql)
        rows = database.executeNonQueryRows(sql)
        return rows

    def deleteFundador(self, idFundador):
        database = self.get_databaseXObj()
        sql = f"delete from fishingdb.fundador where fundador.id = '{idFundador}';"
        rows = database.executeNonQueryRows(sql)
        return rows

    def getHistoria(self, idEmprendimiento):
        dataBase = self.get_databaseXObj()
        sql = (
            "select fishingdb.emprendimiento.historia from fishingdb.emprendimiento "
            + f"where fishingdb.emprendimiento.id = {idEmprendimiento};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, ["historia"])
        return data

    def getDescripcion(self, idEmprendimiento):
        dataBase = self.get_databaseXObj()
        sql = (
            "select fishingdb.emprendimiento.descripcion from fishingdb.emprendimiento "
            + f"where fishingdb.emprendimiento.id = {idEmprendimiento};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, ["descripcion"])
        return data

    def updateHistoria(self, idEmprendimiento, historia):
        database = self.get_databaseXObj()
        sql = (
            f"UPDATE fishingdb.emprendimiento SET historia = '{historia}' "
            + f"WHERE id = {idEmprendimiento};"
        )
        print(sql)
        rows = database.executeNonQueryRows(sql)
        return rows

    # INFORMACION
    def getContactos(self, idEmprendimiento):
        dataBase = self.get_databaseXObj()
        sql = (
            "select emprendimiento.email, emprendimiento.telefono, emprendimiento.facebook, emprendimiento.instagram, emprendimiento.youtube "
            + "from fishingdb.emprendimiento "
            + f"where fishingdb.emprendimiento.id = {idEmprendimiento};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(
            data, ["email", "telefono", "facebook", "instagram", "youtube"]
        )
        return data

    def updateContactos(
        self, idEmprendimiento, email, telefono, facebook, instagram, youtube
    ):
        database = self.get_databaseXObj()
        sql = (
            f"UPDATE fishingdb.emprendimiento SET email = '{email}', telefono = '{telefono}', facebook = '{facebook}', instagram = '{instagram}', "
            + f"youtube = '{youtube}' WHERE id = {idEmprendimiento};"
        )
        print(sql)
        rows = database.executeNonQueryRows(sql)
        return rows

    def getInfoFinanciera(self, idEmprendimiento):
        dataBase = self.get_databaseXObj()
        sql = (
            "select emprendimiento.inversion_inicial, emprendimiento.fecha_fundacion, emprendimiento.venta_anio_anterior "
            + "from fishingdb.emprendimiento "
            + f"where fishingdb.emprendimiento.id = {idEmprendimiento};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(
            data, ["inversion_inicial", "fecha_fundacion", "venta_año_anterior"],
        )
        return data

    def updateInfoFinanciera(
        self, idEmprendimiento, inversion_inicial, fecha_fundacion, venta_año_anterior,
    ):
        database = self.get_databaseXObj()
        sql = (
            f"UPDATE fishingdb.emprendimiento SET inversion_inicial = '{inversion_inicial}', fecha_fundacion = '{fecha_fundacion}', venta_anio_anterior = '{venta_año_anterior}' "
            + f" WHERE id = {idEmprendimiento};"
        )
        print(sql)
        rows = database.executeNonQueryRows(sql)
        return rows

    # =================================================================================================================

    # Get All
    def getAllEmprendimientosByIdEmprendendor(self, idEmprendedor):
        dataBase = self.get_databaseXObj()

        sql = (
            "select emprendimiento.* "
            + "from fishingdb.emprendimiento inner join fishingdb.fundador on emprendimiento.id = fundador.id_emprendimiento "
            + f"where fundador.id_emprendedor = {idEmprendedor};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data

    # Delete
    def deleteEmprendimientoByIdEmprendimiento(self, id):
        database = self.get_databaseXObj()
        sql = f"delete from fishingdb.emprendimiento where id = '{id}';"
        row = database.executeNonQueryRows(sql)
        return row

    # Imagen
    def saveImagesEmprendimiento(self, id_emprendimiento):
        data = self.getEmprendimientoByIdDiccionary(id_emprendimiento)
        for registro in data:
            foto = registro["foto"]
            nombre_foto = registro["nombre_foto"]
            if nombre_foto != "default.png":
                path = os.getcwd() + "\\static\\images\\emprendimiento\\" + nombre_foto
                with open(path, "wb") as file:
                    file.write(foto)

    def insertFundadorById(self, id_emprendedor, id_emprendimiento):
        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.fundador (id, id_emprendedor, id_emprendimiento) "
            + f"values (0, {id_emprendedor}, {id_emprendimiento});"
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def salirEmprendimiento(self, id_emprendedor, id_emprendimiento):
        database = self.get_databaseXObj()
        sql = f"delete from fishingdb.fundador where id_emprendedor = {id_emprendedor} and id_emprendimiento = {id_emprendimiento};"
        row = database.executeNonQueryRows(sql)
        return row

    def getDatosGeneralesById(self, idEmprendimiento):
        dataBase = self.get_databaseXObj()
        sql = f"select * from fishingdb.emprendimiento where id={idEmprendimiento};"
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data

    def updateDatosGeneralesWithoutFoto(
        self, idEmprendimiento, descripcion, eslogan, nombre, video,
    ):
        database = self.get_databaseXObj()
        sql = f"update fishingdb.emprendimiento set emprendimiento.nombre= '{nombre}',emprendimiento.eslogan= '{eslogan}', "
        sql2 = f"emprendimiento.descripcion= '{descripcion}', emprendimiento.video= '{video}' where emprendimiento.id = '{idEmprendimiento}';"
        rows = database.executeNonQueryRows(sql + sql2)
        return rows

    def updateDatosGeneralesWithFoto(
        self, idEmprendimiento, descripcion, eslogan, nombre, foto, video,
    ):
        database = self.get_databaseXObj()
        sql = (
            "update fishingdb.emprendimiento"
            + " set descripcion = %s, eslogan = %s, nombre = %s, foto = %s, video = %s, nombre_foto = %s"
            + " where id = %s;"
        )
        print(sql)
        data = (
            descripcion,
            eslogan,
            nombre,
            foto,
            video,
            str(idEmprendimiento) + ".png",
            idEmprendimiento,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)
        self.saveImagesEmprendimiento(idEmprendimiento)
        return rows

    def getEmprendimientoByIdDiccionary(self, id):
        dataBase = self.get_databaseXObj()
        sql = (
            "SELECT * FROM fishingdb.emprendimiento "
            + f"where emprendimiento.id = {id};"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        return data

    def getIdEmprendimiento(self, id):
        dataBase = self.get_databaseXObj()
        sql = (
            "SELECT * FROM fishingdb.emprendimiento "
            + f"where emprendimiento.id = {id};"
        )
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            EmprendimientoObj = emprendimientoObj(
                data_dic["id"],
                data_dic["estado"],
                data_dic["descripcion"],
                data_dic["historia"],
                data_dic["eslogan"],
                data_dic["inversion_inicial"],
                data_dic["fecha_fundacion"],
                data_dic["venta_año_anterior"],
                data_dic["nombre"],
                data_dic["nombre_foto"],
                data_dic["foto"],
                data_dic["video"],
                data_dic["email"],
                data_dic["telefono"],
                data_dic["facebook"],
                data_dic["instagram"],
                data_dic["youtube"],
            )
            return EmprendimientoObj
        else:
            return None

    def FundadoresByEmprendimientoCorreo(self, user, id_emprendimiento):
        id_usuario = UserLogic()
        usuario = id_usuario.getUserByUser(user)
        Inversor = inversorLogic()
        id_inversor = Inversor.getIdInversor(usuario.getId())
        dataBase = self.get_databaseXObj()
        Emprendimiento = emprendimientoLogic()
        idEmprendimiento = Emprendimiento.getEmprendimientoById(id_emprendimiento)
        sql = (
            "select id_emprendedor from fishingdb.fundador "
            + f"where id_emprendimiento = {id_emprendimiento};"
        )
        print(sql)
        fundadores = dataBase.executeQuery(sql)
        listaFundadores = []
        for registro in fundadores:
            sql2 = (
                "insert into fishingdb.notificaciones (idnotificaciones, mensaje, id_emprendedor, fecha, hora) "
                + f"values (0, 'El inversionista {id_inversor.getNombre()} te ha enviado un mensaje. "
                + f"Está interesado en el emprendimiento: {idEmprendimiento.getNombre()}', {registro[0]}, "
                + "current_date(), current_time());"
            )
            print(sql2)
            rows = dataBase.executeNonQueryRows(sql2)
            currentList = list(registro)
            listaFundadores.append(currentList[0])
        return listaFundadores

    def getNewIdEmprendimiento(self, nombre, eslogan, fecha_fundacion):
        database = self.get_databaseXObj()
        sql2 = (
            f"select emprendimiento.id from fishingdb.emprendimiento "
            + f"where emprendimiento.nombre = '{nombre}' and emprendimiento.eslogan = '{eslogan}' and emprendimiento.fecha_fundacion = '{fecha_fundacion}'"
        )
        data = database.executeQuery(sql2)
        return data[0][0]

    def insertEspecialidad(self, idEmprendimiento, idCategoria):
        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.especialidad (id, id_emprendimiento, id_categoria) "
            + f"values (0, {idEmprendimiento}, {idCategoria});"
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def updateEmprendimiento(
        self,
        idEmprendimiento,
        estado,
        descripcion,
        historia,
        eslogan,
        inversion_inicial,
        fecha_fundacion,
        venta_año_anterior,
        nombre,
        foto,
        video,
        email,
        telefono,
        facebook,
        instagram,
        youtube,
    ):
        database = self.get_databaseXObj()
        sql = (
            "update fishingdb.emprendimiento"
            + " set estado = %s, descripcion = %s, historia = %s, eslogan = %s, inversion_inicial = %s, fecha_fundacion = %s, venta_anio_anterior = %s, "
            + "nombre = %s, foto = %s, video = %s, email = %s, telefono = %s, facebook = %s, instagram = %s, youtube = %s, "
            + "nombre_foto = %s "
            + "where id = %s;"
        )
        print(sql)
        data = (
            estado,
            descripcion,
            historia,
            eslogan,
            inversion_inicial,
            fecha_fundacion,
            venta_año_anterior,
            nombre,
            foto,
            video,
            email,
            telefono,
            facebook,
            instagram,
            youtube,
            str(idEmprendimiento) + ".png",
            idEmprendimiento,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)
        self.saveImagesEmprendimiento(idEmprendimiento)

    def updateEmprendimientoWitoutPhoto(
        self,
        idEmprendimiento,
        estado,
        descripcion,
        historia,
        eslogan,
        inversion_inicial,
        fecha_fundacion,
        venta_año_anterior,
        nombre,
        video,
        email,
        telefono,
        facebook,
        instagram,
        youtube,
    ):
        database = self.get_databaseXObj()
        sql = (
            "update fishingdb.emprendimiento "
            + "set estado = %s, descripcion = %s, historia = %s, eslogan = %s, inversion_inicial = %s, fecha_fundacion = %s, venta_anio_anterior = %s, "
            + "nombre = %s, video = %s, email = %s, telefono = %s, facebook = %s, instagram = %s, youtube = %s "
            + "where id = %s;"
        )
        print(sql)
        data = (
            estado,
            descripcion,
            historia,
            eslogan,
            inversion_inicial,
            fecha_fundacion,
            venta_año_anterior,
            nombre,
            video,
            email,
            telefono,
            facebook,
            instagram,
            youtube,
            idEmprendimiento,
        )
        rows = database.executeNonQueryRowsTuple(sql, data)

    def getIdEmprendedorByUser(self, user):
        database = self.get_databaseXObj()
        sql = (
            "select emprendedor.id from fishingdb.emprendedor inner join fishingdb.usuario "
            + "on emprendedor.id_usuario = usuario.id "
            + f"where usuario.usuario = '{user}';"
        )
        data = database.executeQuery(sql)
        return data[0][0]
