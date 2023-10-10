import pygame
import sys
import time
from Arbol import *

"""
FUNCIONES PRINCIPALES___________________________________________________"""
# Función que dibuja al meñeco
def dibujar_muneco():
    ventana.blit(muneco_img, (pos_x * TAMANO_CUADRO, pos_y * TAMANO_CUADRO))

# Funcion que visualiza los alrededores del muñeco
def sensor_mirar():
    areas_descubiertas[pos_y][pos_x] = True
    Lista_areas_descubiertas = [None]  # Guardamos aquí una lista de las areas descubiertas
    Lista_Auxiliar = [None]   # ALmacena la posición de las areas


    if pos_y - 1 >= 0: # Arriba
        areas_descubiertas[pos_y - 1][pos_x] = True
        Lista_Auxiliar = Nodo(pos_y - 1, pos_x, 'Arriba')
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    if pos_y + 1 < len(matriz):  # Abajo
        areas_descubiertas[pos_y + 1][pos_x] = True
        Lista_Auxiliar = Nodo(pos_y + 1, pos_x, 'Abajo')
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    if pos_x + 1 < len(matriz[0]): # Derecha
        areas_descubiertas[pos_y][pos_x + 1] = True
        Lista_Auxiliar = Nodo(pos_y, pos_x + 1, 'Derecha')
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    if pos_x - 1 >= 0: # Izquierda
        areas_descubiertas[pos_y][pos_x - 1] = True
        Lista_Auxiliar = Nodo(pos_y, pos_x - 1, 'Izquierda')
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    areas_visitadas[pos_y][pos_x] = True

    # Eliminamos aquellos valores en la lista con valores nulos
    Lista_Auxiliar_2 = []
    aux = 0

    # Recorremos la lista de areas visitadas en busqueda de iteraciones vacias
    for i in range(len(Lista_areas_descubiertas)):
        if Lista_areas_descubiertas[i] == None:
            Lista_Auxiliar_2.append(i)  # Almacenamos su posición en una lista extra

    else:  # Eliminamos esos elementos que no nos sirvan
        for i in range(len(Lista_Auxiliar_2)):
            Lista_areas_descubiertas.pop(i)
            Lista_Auxiliar_2.pop()
            i-= 1

            if  (i + 1 == len(Lista_Auxiliar_2) or len(Lista_Auxiliar_2) == 0): break

    return Lista_areas_descubiertas

"""
PARAMETROS INICIALES____________________________________________________"""
# Macros
TAMANO_CUADRO = 30    # Tamaño de los cuadros
TAMANO_MUNEQUITO = 17 # Tamaño del muñeco

BLANCO = (255, 255, 255)    # Color blanco
NEGRO = (0, 0, 0)           # Color negro
GRIS = (128, 128, 128)      # Color gris

matriz = []    # Matriz del laberinto
ganado = False # Condicion principal

# Coordenadas iniciales del muñequito
pos_x = 0
pos_y = 9

"""
GENERAR MATRIZ__________________________________________________________"""

# Abre la matriz de lectura y lee la matriz
with open('./Laberinto.txt', 'r') as f: lineas = f.readlines()

# Iterar a través de las líneas y crear una lista de listas (matriz)
for linea in lineas:
    fila = [int(valor) for valor in linea.strip().split(',')]
    matriz.append(fila)

# Dimensiones de la ventana
ANCHO = len(matriz[0]) * TAMANO_CUADRO
ALTO = len(matriz) * TAMANO_CUADRO


"""
INICIALIZAR PYGAME Y CARGAR VALORES_____________________________________"""
# Inicializar pygame
pygame.init()

# Crear ventana
ventana = pygame.display.set_mode((ANCHO, ALTO)) # Generar ventana
pygame.display.set_caption("Laberinto")          # Nombre de la ventana

# Cargar la imagen del muñeco y redimensionarla
muneco_img = pygame.Surface((TAMANO_MUNEQUITO, TAMANO_MUNEQUITO))
muneco_img.fill(BLANCO)
muneco_img.set_colorkey(BLANCO)
pygame.draw.circle(muneco_img, NEGRO, (TAMANO_MUNEQUITO // 2, TAMANO_MUNEQUITO // 2), TAMANO_MUNEQUITO // 2)
muneco_img = muneco_img.convert_alpha()

# Cargando fuentes
fuente_v = pygame.font.Font(None, 24) # Fuente de 'v' de visitado
fuente = pygame.font.Font(None, 20)   # Fuente de coordenadas generales

# Crear e inicializar una matriz para rastrear las áreas visitadas por el muñeco
areas_visitadas = [[False for _ in fila] for fila in matriz]

# Crear e inicializar una matriz para rastrear las áreas descubiertas
areas_descubiertas = [[False for _ in fila] for fila in matriz]

# Texto para fuente de V
letra_v = fuente_v.render('V', True, NEGRO) # Dibujar texto


"""
EJECUCIÓN DEL CÓDIGO____________________________________________________"""

#Creamos el arbol de desición con un nodo inicial
ARBOL = Arbol()
"""Posicion_inicial = [pos_y, pos_x]
ARBOL.Agregar_nodo_LIFO(Nodo(pos_y, pos_x))
ARBOL.Agregar(Posicion_inicial)"""


# Generar arbol y dibujar
while True:
    areas_descubiertas[pos_y][pos_x] = True
    Direccion = None

    Nodos_por_agregar = []       # Guardar los nodos en una lista para despues agregarlos todos al LIFO
    Posiciones_por_agregar = []  # Parametro principal de generar_nodos




    if ARBOL.Vacio():
        Posicion_inicial = [pos_y, pos_x]
        ARBOL.Agregar_nodo_LIFO(Nodo(pos_y, pos_x))
        ARBOL.Generar_nodos(None)

    else:
        # 1. ANALISIS DE LOS LADOS
        Areas_Visitadas = sensor_mirar()  # Adquirimos las areas descubiertas

        # 2. FILTRAR LADOS
        # Agregamos los nodos a los que podemos avanzar en un LIFO queue
        for i in range(len(Areas_Visitadas)):

            # almacenamos los nodos a los que solo hay que avanzar
            if matriz[Areas_Visitadas[i].Posicion_y][Areas_Visitadas[i].Posicion_x] == 1:
                if ((Areas_Visitadas[i].Posicion_actual in ARBOL.Nodos_recorridos) is False) or (len(Arbol.Nodos_recorridos) == 0):
                    nodo = Nodo(Areas_Visitadas[i].Posicion_Y, Areas_Visitadas[i].Posicion_X, Areas_Visitadas[i].direccion)
                    ARBOL.Agregar_nodo_LIFO(nodo)
                    ARBOL.Generar_nodos(Areas_Visitadas[i].direccion)
                    ARBOL.Agregar_direccion_nodo(nodo.direccion)
                    Direccion = nodo.direccion

                    time.sleep(1)


    #EXPANDIR NODOS DISPONIBLES

    """    # Recorremos la lista de nodos para avanzar y generar las hojas
        for i in range(ARBOL.Numero_nodos_analizar()):
            nodo = ARBOL.Nodo_analizar()
    
            if (nodo in ARBOL.Lista_nodos_recorridos() == True):
                continue
    
            else:
                ARBOL.Agregar_nodos()
    
    """


    if pos_x == 14 and pos_y == 1: ganado = True  # De haber llegado a las coordenadas finales

    """
    AGENO A MI__________________________________________________________"""

    # Dibujar el laberinto
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            if not areas_descubiertas[fila][columna]:
                color = GRIS  # Si no se ha descubierto, pintar de gris

            else: color = BLANCO if matriz[fila][columna] == 1 else NEGRO

            pygame.draw.rect(ventana, color, (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
            if areas_visitadas[fila][columna]:
                letra_v_rect = letra_v.get_rect()
                letra_v_rect.topleft = (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO)
                ventana.blit(letra_v, letra_v_rect)



    # En caso de haber llegado al punto final
    if ganado:
        mensaje = '¡Haz ganado!'
        fuente_ganado = pygame.font.Font(None, 36)
        mensaje_renderizado = fuente_ganado.render(mensaje, True, BLANCO)
        ventana.blit\
            (mensaje_renderizado,
             (
                 ANCHO // 2 - mensaje_renderizado.get_width() // 2,
                 ALTO // 2 - mensaje_renderizado.get_height() // 2
             )
            )

        pygame.display.update()
        pygame.time.delay(5000)  # Espera 5 segundos

        pygame.quit()
        sys.exit()

    # Mostrar coordenadas generales en la ventana
    coordenadas = f'Coordenadas: ({pos_x}, {pos_y})'
    texto = fuente.render(coordenadas, True, BLANCO)
    ventana.blit(texto, (10, 10))
    pygame.display.update()

    dibujar_muneco()  # Dibujar el muñeco

    if Direccion == "Arriba":  pos_y -= 1
    if Direccion == "Abajo":   pos_y += 1
    if Direccion == "Derecha": pos_x += 1
    if Direccion == "Izquierda": pos_x -= 1

    # Coordenadas de inicio.
    inicio_i = f'In'
    ini_i = fuente.render(inicio_i, True, NEGRO)
    ventana.blit(ini_i, (0, 9 * TAMANO_CUADRO))  # Coordenadas (0, 9) multiplicadas por el tamaño de cuadro

    inicio_f = f'F'
    ini_f = fuente.render(inicio_f, True, NEGRO)
    ventana.blit(ini_f,
                 (14 * TAMANO_CUADRO, 1 * TAMANO_CUADRO))  # Coordenadas (14, 1) multiplicadas por el tamaño de cuadro

    pygame.display.update()