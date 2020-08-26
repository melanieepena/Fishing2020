class emprendimientoObj:
    def __init__(
        self,
        id,
        estado,
        descripcion,
        historia,
        eslogan,
        inversion_inicial,
        fecha_fundacion,
        venta_año_anterior,
        nombre,
        nombre_foto,
        foto,
        video,
        email,
        telefono,
        facebook,
        instagram,
        youtube,
    ):
        self.id = id
        self.estado = estado
        self.descripcion = descripcion
        self.historia = historia
        self.eslogan = eslogan
        self.inversion_inicial = inversion_inicial
        self.fecha_fundacion = fecha_fundacion
        self.venta_año_anterior = venta_año_anterior
        self.nombre = nombre
        self.nombre_foto = nombre_foto
        self.foto = foto
        self.video = video
        self.email = email
        self.telefono = telefono
        self.facebook = facebook
        self.instagram = instagram
        self.youtube = youtube

    def getId(self):
        return self.id

    def getNombre(self):
        return self.nombre

    def getEmail(self):
        return self.email
