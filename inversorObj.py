class inversorObj:
    def __init__(
        self, id, nombre, biografia, email, usuario, pais, ciudad, foto, nombre_foto
    ):
        self.id = id

        self.nombre = nombre
        self.biografia = biografia
        self.email = email
        self.pais = pais
        self.ciudad = ciudad
        self.usuario = usuario
        self.foto = foto
        self.nombre_foto = nombre_foto

    def getId(self):
        return self.id

    def getNombre(self):
        return self.nombre

    def getEmail(self):
        return self.email
