class UserObj:
    def __init__(self, id, user, password, rol):
        self.id = id
        self.user = user
        self.password = password
        self.rol = rol

    def getId(self):
        return self.id

    def getUser(self):
        return self.user
