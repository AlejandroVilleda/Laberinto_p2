import pygame
import sys
import time
from Arbol_1 import *

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
        Lista_Auxiliar = [pos_y - 1, pos_x, 'Arriba']
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    if pos_y + 1 < len(matriz):  # Abajo
        areas_descubiertas[pos_y + 1][pos_x] = True
        Lista_Auxiliar = [pos_y + 1, pos_x, 'Abajo']
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    if pos_x + 1 < len(matriz[0]): # Derecha
        areas_descubiertas[pos_y][pos_x + 1] = True
        Lista_Auxiliar = [pos_y, pos_x + 1, 'Derecha']
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    if pos_x - 1 >= 0: # Izquierda
        areas_descubiertas[pos_y][pos_x - 1] = True
        Lista_Auxiliar = [pos_y, pos_x - 1, 'Izquierda']
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    areas_visitadas[pos_y][pos_x] = True

    # Eliminamos aquellos valores en la lista con valores nulos
    Lista_Auxiliar_2 = []
    aux = 0

    for i in range(len(Lista_areas_descubiertas)):
        if Lista_areas_descubiertas[i] == None:
            Lista_Auxiliar_2.append(i)

    else:
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
Posicion_inicial = [pos_y, pos_x]
ARBOL.Agregar(Posicion_inicial)


# Generar arbol y dibujar
while True:
    time.sleep(1)
    Areas_Visitadas = sensor_mirar()  # Adquirimos las areas descubiertas
    Posicion_Auxiliar = [None]        # almacena de forma temporal la posición a dirigirse

    # Valoramos los valores de cada uno de los camidos descubiertos
    for i in range(len(Areas_Visitadas)):
        if (matriz[Areas_Visitadas[i][0]][Areas_Visitadas[i][1]] == 1) and ([Areas_Visitadas[i][0], Areas_Visitadas[i][1]] != ARBOL.Valor_Padre): # Si el area en particular es un camino, lo agregamos como nodo al arbol
            ARBOL.Agregar(Areas_Visitadas[i]) # Generamos nodo
            Posicion_Auxiliar = Areas_Visitadas[i]

    Numero_hijos = ARBOL.Contar_Hijos() # Contamos el número de nodos generados


    if pos_x == 14 and pos_y == 1: ganado = True  # De haber llegado a las coordenadas finales

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

    # Dibujar el muñeco
    dibujar_muneco()
    """Desplazamiento del muñeco"""
    # Si hay un solo nodo hijo, iremos directo hacia él
    if Numero_hijos == 1:
        # ARBOL.Avanzar()     # Avanzamos al siguiente nodo

        # Actualizamos las coordenadas para continuar con el camino en el laberinto

        if Posicion_Auxiliar[2] == 'Arriba':
            pos_y -= 1

        elif Posicion_Auxiliar[2] == 'Abajo':
            pos_y += 1

        elif Posicion_Auxiliar[2] == 'Derecha':
            pos_x += 1

        elif Posicion_Auxiliar[2] == 'Izquierda':
            pos_x -= 1

    # De haber más de un hijo, seleccionamos uno bajo el siguiente orden: Arriba, Abajo, derecha u Izquierda
    elif Numero_hijos > 1:

        for i in range(len(Areas_Visitadas)):
            # Escogemos 'Arriba'
            if ('Arriba' in Areas_Visitadas[i][2]):
                ARBOL.Avance_particular('Arriba')
                pos_y -= 1
                break

            # Escogemos 'Abajo'
            elif ('Abajo' in Areas_Visitadas[i][2]):
                ARBOL.Avance_particular('Abajo')
                pos_y += 1
                break

            # Escogemos 'Derecha'
            elif ('Derecha' in Areas_Visitadas[i][2]):
                ARBOL.Avance_particular('Derecha')
                pos_x += 1
                break

            # Escogemos 'Izquierda'
            elif ('Izquierda' in Areas_Visitadas[i][2]):
                ARBOL.Avance_particular('Izquierda')
                pos_x -= 1
                break

    else:  # De no haber ningun nodo hijo, estamos en una hoja, por lo tanto, regresamos
        pass

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

    # Coordenadas de inicio.
    inicio_i = f'In'
    ini_i = fuente.render(inicio_i, True, NEGRO)
    ventana.blit(ini_i, (0, 9 * TAMANO_CUADRO))  # Coordenadas (0, 9) multiplicadas por el tamaño de cuadro

    inicio_f = f'F'
    ini_f = fuente.render(inicio_f, True, NEGRO)
    ventana.blit(ini_f,
                 (14 * TAMANO_CUADRO, 1 * TAMANO_CUADRO))  # Coordenadas (14, 1) multiplicadas por el tamaño de cuadro

    pygame.display.update()