import collections

class Agente:
    # Constructor del agente en una posición de la matriz
    def __init__(self, posicion):
        self.posicion = posicion  # La posición inicial del agente

# Función auxiliar, recibe un laberinto y regresa la posición de entrada
def encontrar_entrada(laberinto):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == "E":
                return (fila, columna)
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


#Función que encuentra vecinos válidos dado una coordenada y un laberinto
# Un vecino es válido cuando:
# *Es un movimiento válido
# *No es una pared
# *No está en la lista de visitados
def encuentra_vecinos(pos,laberinto,visitados):
    vecinos = []
    x, y = pos
    if x > 0  and laberinto[x-1][y] != 1 and (not (x-1,y) in visitados):                     #Arriba
        vecinos.append((x-1,y))
    if x < len(laberinto) - 1 and laberinto[x+1][y] != 1 and (not (x+1,y) in visitados):     #Abajo
        vecinos.append((x+1,y))
    if y > 0 and laberinto[x][y-1] != 1 and (not (x,y-1) in visitados):                      #Izq
        vecinos.append((x,y-1))
    if y < len(laberinto[0]) - 1 and laberinto[x][y+1] != 1 and (not (x,y+1) in visitados):  #Der
        vecinos.append((x,y+1))
    return vecinos

def salida_BFS(agente,laberinto):
  #Lista de coordenadas visitadas
  visitados = []

  #Cola de coordenadas
  cola = []

  #Ruta seguida
  ruta = {}
  final = (-1,-1)
  inicio = agente.posicion

  #Inicializamos la cola con la entrada del laberinto
  visitados.append(inicio)
  cola.append(inicio)

  #Loop
  #Hacemos pop en la cola y revisamos sus vecinos posibles, si existen se agregan
  #A la cola y a la lista de visitados
  #Quitar los comentarios de los print si se quiere ver el análisis completo
  while cola:
    #print("===================================")
    #print("Cola al inicio del paso:", cola)
    actual = cola.pop(0)


    #Condición de salida, Encontramos la salida
    if laberinto[actual[0]][actual[1]] == "S":
        #print("Se encontró una salida!")
        final = (actual[0],actual[1])
        break
    #Buscamos vecinos válidos
    vecinos = encuentra_vecinos([actual[0],actual[1]],laberinto,visitados)
    #Si se encontraron se agregan y tambíen se marca una posible ruta dentro del
    #Diccionario
    for vecino in vecinos:
      visitados.append(vecino)
      cola.append(vecino)
      #Con esto nos aseguramos de encontrar la ruta más corta
      ruta[vecino] = actual
      #print("Se agregó al vecino :",vecino)

    #print("Visitados: ", visitados)
    #print("Cola al final del paso:", cola)
    #print("===================================")

  #Una si la cola se vació, tenemos 2 casos, o existe una ruta o no hay ruta
  #Se invierte la ruta
  if final == (-1,-1):
    return {}
  else:
    rutafinal={}
  #Se invierte la ruta
    while final != inicio:
      rutafinal[ruta[final]]=final
      final=ruta[final]
    return rutafinal

def salida_DFS(agente,laberinto):
  #Lista de coordenadas visitadas
  visitados = []

  #Pila de coordenadas
  pila = []

  #Ruta seguida
  ruta = {}
  final = (-1,-1)
  inicio = agente.posicion

  #Inicializamos la pila con la entrada del laberinto
  visitados.append(inicio)
  pila.append(inicio)

  #Loop
  #Hacemos pop en la pila y revisamos sus vecinos posibles, si existen se agregan
  #A la pila y a la lista de visitados
  #Quitar los comentarios de los print si se quiere ver el análisis completo
  while pila:
    #print("===================================")
    #print("Pila al inicio del paso:", pila)
    actual = pila.pop()


    #Condición de salida, Encontramos la salida
    if laberinto[actual[0]][actual[1]] == "S":
        #print("Se encontró una salida!")
        final = (actual[0],actual[1])
        break
    #Buscamos vecinos válidos
    vecinos = encuentra_vecinos([actual[0],actual[1]],laberinto,visitados)
    #Si se encontraron se agregan y tambíen se marca una posible ruta dentro del
    #Diccionario
    for vecino in vecinos:
      visitados.append(vecino)
      pila.append(vecino)
      ruta[vecino] = actual
      #print("Se agregó al vecino :",vecino)

    #print("Visitados: ", visitados)
    #print("Pila al final del paso:", pila)
    #print("===================================")


  #Una si la pila se vació, tenemos 2 casos, o existe una ruta o no hay ruta

  if final == (-1,-1):
    return {}
  else:
    rutafinal={}
  #Se invierte la ruta
    while final != inicio:
      rutafinal[ruta[final]]=final
      final=ruta[final]
    return rutafinal




#Función para imprimir la ruta del diccionario en orden
def imprime_ruta(ruta,inicio):
  actual = inicio
  respuesta = str(actual)
  while ruta:
    actual = ruta.pop(actual)
    respuesta = respuesta + " -> "  +str(actual)
  return respuesta

#Caso laberinto pequeño con salida
laberinto = [
    ["E", 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 0, "S"]
]

#Caso laberinto pequeño con salida
laberinto2 =  [
    ["E", 0, 0],
    [0,1, 0],
    [0,1, "S"]
]


#Caso laberinto pequeño sin salida
laberinto3 = [
    ["E", 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 0, 0]
]



#Caso laberinto grande
laberinto4 = [
    [0, 0, 0,1, "S"],
    [0, 1, 0,1 , 0],
    [0, 1, 0,1 ,0],
    [0, 1, 0,1, 0],
    [0, 1, 0,1, 0],
    ["E", 0, 0,0, 0]
]

#Cambiar en nombre del laberinto para elegir
caso = parse_laberinto(laberinto4)  # <---- aca
entrada = encontrar_entrada(caso)
agente = Agente(entrada)
salida = salida_BFS(agente, caso)
if salida == {}:
  print("No se encontró una salida")
else:
  print("Para el laberinto:")
  print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in caso]))
  print("La ruta encontrada es: ")
  print(imprime_ruta(salida,agente.posicion))
