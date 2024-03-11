import heapq

class Agente:
    def __init__(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin

def encontrar_entrada(laberinto):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == "E":
                return (fila, columna)
    return None

def encontrar_salida(laberinto):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == "S":
                return (fila, columna)
    return None

def parse_laberinto(laberinto):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == '0':
                laberinto[fila][columna] = 0
            if laberinto[fila][columna] == '1':
                laberinto[fila][columna] = 1
    return laberinto

def distancia_manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_costo_g(ruta, actual):
    return ruta.get(actual, (0,0))[0] + 1

def get_costo_h(vecino, fin):
    return distancia_manhattan(vecino, fin)

def get_costo_f(g,h):
    return g + h

def encuentra_vecinos(pos, laberinto, visitados):
    vecinos = []
    x, y = pos
    if x > 0  and laberinto[x-1][y] != 1 and (not (x-1,y) in visitados):
        vecinos.append((x-1, y))
    if x < len(laberinto) - 1 and laberinto[x+1][y] != 1 and (not (x+1, y) in visitados):
        vecinos.append((x+1, y))
    if y > 0 and laberinto[x][y-1] != 1 and (not (x, y-1) in visitados):
        vecinos.append((x, y-1))
    if y < len(laberinto[0]) - 1 and laberinto[x][y+1] != 1 and (not (x, y+1) in visitados):
        vecinos.append((x, y+1))
    return vecinos

def encuentra_salida(agente, laberinto):
    visitados = []
    cola_prioridad = []
    ruta = {}
    inicio = agente.inicio
    fin = agente.fin

    heapq.heappush(cola_prioridad, (0, inicio))

    while cola_prioridad:
        _, actual = heapq.heappop(cola_prioridad)

        if actual == fin:
            break

        vecinos = encuentra_vecinos(actual, laberinto, visitados)

        for vecino in vecinos:
            costo_g = get_costo_g(ruta, actual)
            costo_h = get_costo_h(vecino, fin)
            costo_f = get_costo_f(costo_g, costo_h)

            if vecino not in ruta or costo_f < ruta[vecino][1]:
                ruta[vecino] = (costo_g, costo_f, actual)
                heapq.heappush(cola_prioridad, (costo_f, vecino))
    
    if actual != fin:
        return {}, -1
    else:
        ruta_final = reconstruir_ruta(ruta, inicio, fin)
        costo_final = ruta[fin][0]
        return ruta_final, costo_final

def reconstruir_ruta(ruta, inicio, fin):
    ruta_final = []
    actual = fin
    
    while actual != inicio:
        ruta_final.append((actual))
        # Sigue el nodo hacia atrás
        actual = ruta[actual][2]

    # Agrega el nodo de inicio a la ruta
    ruta_final.append((inicio))
    ruta_final.reverse()
    
    return ruta_final

laberinto = [
    [0, 0, 0, 1, "S"],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 1, 0],
    ["E", 0, 0, 0, 0]
]

laberinto = parse_laberinto(laberinto)
entrada = encontrar_entrada(laberinto)
salida = encontrar_salida(laberinto)
agente = Agente(entrada, salida)
ruta, costo = encuentra_salida(agente, laberinto)

if ruta == {}:
    print("No se encontró una salida")
else:
    print("Para el laberinto:")
    for row in laberinto:
        print('\t'.join([str(cell) for cell in row]))
    print("La ruta encontrada es: ")
    print(ruta)
    print("El costo de la ruta es:", costo)
