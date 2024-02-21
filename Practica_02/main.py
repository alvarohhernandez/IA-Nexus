import collections

laberinto = [
    ["E", 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 0, "S"]
]

# Creamos una matriz auxiliar de tamaño igual al laberinto, para almacenar los puntos visitados
visitado = [[False] * len(laberinto[0]) for _ in range(len(laberinto))]

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
            exit()

        elif agente.mover(movimiento, laberinto) != 0:
            encontrar_salida(agente, laberinto, ruta_seguida)
            agente.mover(movimiento, laberinto)  # Deshacer el movimiento
            ruta_seguida.pop()  # Deshacer el movimiento en la ruta

        elif agente.mover(movimiento, laberinto) == 0:
            contador += 1
            if contador == 4:
                ruta_seguida.pop()
                if not ruta_seguida:
                    print("No existe una salida :(")
                    exit()
                ultimo = ruta_seguida[-1]
                ruta_seguida.pop()
                back = Agente([ultimo[0], ultimo[1]])
                encontrar_salida(back, laberinto, ruta_seguida)

    print("iiiiii no encontré la salida")

# Función auxiliar, recibe un laberinto y regresa la posición de entrada
def encontrar_entrada(laberinto):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == "E":
                return [fila, columna]
    return None

# Función auxiliar, recibe un laberinto y lo regresa estandarizado
def parse_laberinto(laberinto):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == '0':
                laberinto[fila][columna] = 0
            if laberinto[fila][columna] == '1':
                laberinto[fila][columna] = 1
    return laberinto

# Hacemos parsing del laberinto para estandarizar los valores '0' y '1' a 0 y 1
laberinto = parse_laberinto(laberinto)
# Obtenemos la posición de entrada del laberinto
entrada = encontrar_entrada(laberinto)
print(f"Entrada: {entrada}")
# Crear una instancia de la clase Agente
agente = Agente(entrada)
# Marcamos la posición inicial como visitada en la matriz de visitados
visitado[agente.posicion[0]][agente.posicion[1]] = True
ruta = collections.deque([])

# Llamar a la función para encontrar la salida
encontrar_salida(agente, laberinto, ruta)

