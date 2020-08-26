class especialidadObj:
    def __init__(self, id, id_emprendimiento, id_categoria):
        self.id = id

        self.id_emprendimiento = id_emprendimiento
        self.id_categoria = id_categoria

    def getId(self):
        return self.id
