# Representación del laberinto
import queue


laberinto = [
    ["E", 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 0, "S"]
]

class Agente:
    #Constructor del agente en una posicion de la matriz
    def __init__(self, posicion):
        self.posicion = posicion  # La posición inicial del agente

    # Función que permite mover al agente dentro de la matriz
    def mover(self, direccion, laberinto):
        x, y = self.posicion
        if direccion == "arriba" and x > 0 and laberinto[x-1][y] == 0 :
            laberinto[x][y] = 2
            self.posicion = [x-1, y]
        elif direccion == "abajo" and x < len(laberinto) - 1 and laberinto[x+1][y] == 0 :
            self.posicion = [x+1, y]
            laberinto[x][y] = 2
        elif direccion == "izquierda" and y > 0 and laberinto[x][y-1] == 0 :
            self.posicion = [x, y-1]
            laberinto[x][y] = 2
        elif direccion == "derecha" and y < len(laberinto[0]) - 1 and laberinto[x][y+1] == 0 :
            self.posicion = [x, y+1]
            laberinto[x][y] = 2
        else:
            return 0

def encontrar_salida(agente, laberinto, ruta_seguida):
    movimientos = ["arriba", "abajo", "izquierda", "derecha"]
    ruta_seguida.put(agente.posicion.copy()) # Almacena la posición actual en la ruta
    print("Ruta seguida por el agente:", list(ruta_seguida.queue))
    contador= 0

    for movimiento in movimientos:
        if agente.mover(movimiento, laberinto) != 0:
            agente.mover(movimiento, laberinto)
            encontrar_salida(agente, laberinto, ruta_seguida)

        if agente.mover(movimiento, laberinto) == 0:
            contador+= 1
            if contador == 4 :
                ultimo = ruta_seguida.get
                back = Agente(ultimo)
                encontrar_salida(back, laberinto, ruta_seguida)

        if laberinto[agente.posicion[0]][agente.posicion[1]] == "S":
            print("Encontré la salida :D")
            print("Ruta seguida por el agente:", ruta_seguida)
            return

    print("iiiiii no encontré la salida")

# Crear una instancia de la clase Agente
agente = Agente([0, 0])
ruta = queue.LifoQueue(100)

# Llamar a la función para encontrar la salida
encontrar_salida(agente, laberinto, ruta)
