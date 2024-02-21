import collections

laberinto = [
    ["E", 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 0, "S"]
]
visitado = [
    [True, False, False, False],
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False]
]

class Agente:
    # Constructor del agente en una posición de la matriz
    def __init__(self, posicion):
        self.posicion = posicion  # La posición inicial del agente

    # Función que permite mover al agente dentro de la matriz
    def mover(self, direccion, laberinto):
        x, y = self.posicion
        if direccion == "arriba" and x > 0 and laberinto[x-1][y] != 1 and not visitado[x-1][y]:
            visitado[x-1][y] = True
            self.posicion = [x-1, y]
            return 1
        elif direccion == "abajo" and x < len(laberinto) - 1 and laberinto[x+1][y] != 1 and not visitado[x+1][y]:
            self.posicion = [x+1, y]
            visitado[x+1][y] = True
            return 1
        elif direccion == "izquierda" and y > 0 and laberinto[x][y-1] != 1 and not visitado[x][y-1]:
            self.posicion = [x, y-1]
            visitado[x][y-1] = True
            return 1
        elif direccion == "derecha" and y < len(laberinto[0]) - 1 and laberinto[x][y+1] != 1 and not visitado[x][y+1]:
            self.posicion = [x, y+1]
            visitado[x][y+1] = True
            return 1
        else:
            return 0  # Indica que el movimiento no fue válido

def encontrar_salida(agente, laberinto, ruta_seguida):
    movimientos = ["arriba", "abajo", "izquierda", "derecha"]
    ruta_seguida.append(agente.posicion.copy())  # Almacena la posición actual en la ruta
    contador = 0

    for movimiento in movimientos:
        if laberinto[agente.posicion[0]][agente.posicion[1]] == "S":
            print("Encontré la salida :D")
            print("Ruta seguida por el agente:", ruta_seguida)
            return

        elif agente.mover(movimiento, laberinto) != 0:
            encontrar_salida(agente, laberinto, ruta_seguida)
            agente.mover(movimiento, laberinto)  # Deshacer el movimiento
            ruta_seguida.pop()  # Deshacer el movimiento en la ruta

        elif agente.mover(movimiento, laberinto) == 0:
            contador += 1
            if contador == 4:
                ruta_seguida.pop()
                ultimo = ruta_seguida[-1]
                ruta_seguida.pop()
                back = Agente([ultimo[0], ultimo[1]])
                encontrar_salida(back, laberinto, ruta_seguida)

    print("iiiiii no encontré la salida")

# Crear una instancia de la clase Agente
agente = Agente([0, 0])
ruta = collections.deque([])

# Llamar a la función para encontrar la salida
encontrar_salida(agente, laberinto, ruta)

