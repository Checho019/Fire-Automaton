class Arboles:

    # Estados
    # 0 = Arboles quemados
    # 1 = Arboles vivos
    # 2 = Arboles con fuego
    def __init__(self, densidad: float, combustible: float, humedad: float):
        # Variables iniciales del arbol
        self.densidad = densidad
        self.combustible = combustible
        self.humedad = humedad
        self.estado = 1
        self.porcentaje = 100

        # Variables de accion
        self.fuego = {
            "copa":None,
            "superficial":None
        }


    def mostrar_arbol(self):
        print("arbolito :)")
