class productoObj:
    def __init__(
        self,
        id,
        nombre,
        nombre_foto,
        foto,
        descripcion,
        costo_unitario,
        precio_venta,
        patente,
        id_emprendimiento,
    ):
        self.id = id

        self.nombre = nombre
        self.descripcion = descripcion
        self.costo_unitario = costo_unitario
        self.precio_venta = precio_venta
        self.patente = patente
        self.id_emprendimiento = id_emprendimiento
        self.foto = foto
        self.nombre_foto = nombre_foto

    def getId(self):
        return self.id
