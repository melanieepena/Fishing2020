from logic import Logic
from userObj import UserObj


class UserLogic(Logic):
    def __init__(self):
        super().__init__()
        self.keys = ["id", "usuario", "password", "rol"]

    def getUser(self, user, password):
        dataBase = self.get_databaseXObj()
        sql = (
            "SELECT * FROM fishingdb.usuario "
            + f"where usuario.usuario = '{user}' and usuario.password = '{password}';"
        )
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            userObj = UserObj(
                data_dic["id"],
                data_dic["usuario"],
                data_dic["password"],
                data_dic["rol"],
            )
            return userObj
        else:
            return None

    def insertNewUser(self, user, password, rol):
        database = self.get_databaseXObj()
        sql = (
            "insert into fishingdb.usuario (id, usuario, password, rol) "
            + f"values (0, '{user}', '{password}', {rol});"
        )
        rows = database.executeNonQueryRows(sql)
        return rows

    def getNewUser(self, user, password, rol):
        dataBase = self.get_databaseXObj()
        sql = (
            "select * from fishingdb.usuario "
            + f"where usuario = '{user}' and password = '{password}';"
        )
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            usuarioObj = UserObj(
                data_dic["id"],
                data_dic["usuario"],
                data_dic["password"],
                data_dic["rol"],
            )
            return usuarioObj
        else:
            return None

    def checkUserInUsuario(self, user, rol):
        dataBase = self.get_databaseXObj()
        sql = (
            "SELECT usuario.usuario FROM fishingdb.usuario "
            + f"where usuario.usuario = '{user}' and usuario.rol = {rol};"
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

    def createDictionary(self, userObj):
        dictionary = {
            "id": userObj.id,
            "usuario": userObj.user,
            "password": userObj.password,
            "rol": userObj.rol,
        }
        return dictionary

    def getUserByUser(self, user):
        dataBase = self.get_databaseXObj()
        sql = "SELECT * FROM fishingdb.usuario " + f"where usuario.usuario = '{user}';"
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            userObj = UserObj(
                data_dic["id"],
                data_dic["usuario"],
                data_dic["password"],
                data_dic["rol"],
            )
            return userObj
        else:
            return None

    def getUserById(self, id):
        dataBase = self.get_databaseXObj()
        sql = "SELECT * FROM fishingdb.usuario " + f"where usuario.id = '{id}';"
        print(sql)
        data = dataBase.executeQuery(sql)
        data = self.tupleToDictionaryList(data, self.keys)
        if len(data) > 0:
            data_dic = data[0]
            userObj = UserObj(
                data_dic["id"],
                data_dic["usuario"],
                data_dic["password"],
                data_dic["rol"],
            )
            return userObj
        else:
            return None
