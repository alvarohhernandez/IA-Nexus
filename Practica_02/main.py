# Representación del laberinto
laberinto = [
    ["E", 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 0, "S"]
]

class Agente:
    def __init__(self, posicion):
        self.posicion = posicion  # La posición inicial del agente

    def mover(self, direccion, laberinto):
        x, y = self.posicion
        if direccion == "arriba" and x > 0:
            self.posicion = [x-1, y]
        elif direccion == "abajo" and x < len(laberinto) - 1:
            self.posicion = [x+1, y]
        elif direccion == "izquierda" and y > 0:
            self.posicion = [x, y-1]
        elif direccion == "derecha" and y < len(laberinto[0]) - 1:
            self.posicion = [x, y+1]
        else:
            print("El movimiento no es válido D:")

agente = Agente([0,0])

def encontrar_salida(agente, laberinto):
    movimientos = ["derecha", "abajo", "abajo", "derecha", "abajo", "derecha"]

    for movimiento in movimientos:
        agente.mover(movimiento, laberinto)

        print(f"Movimiento: {movimiento}, Posición: {agente.posicion}")

        if laberinto[agente.posicion[0]][agente.posicion[1]] == "S":
            print("Encontré la salida :D")
            return

    print("iiiiii no encontré la salida")

encontrar_salida(agente, laberinto)
