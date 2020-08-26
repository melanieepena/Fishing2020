class emprendedorObj:
    def __init__(
        self,
        id,
        nombre,
        email,
        telefono,
        usuario,
        pais,
        ciudad,
        biografia,
        foto,
        nombre_foto,
    ):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.pais = pais
        self.ciudad = ciudad
        self.usuario = usuario
        self.biografia = biografia
        self.foto = foto
        self.nombre_foto = nombre_foto

    def getId(self):
        return self.id

    def getNombre(self):
        return self.nombre
