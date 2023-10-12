import pygame
import sys
import time
from Arbol import *

"""
FUNCIONES PRINCIPALES___________________________________________________"""

# función creada para trabajar con la inserción de direcciones en orden
def Agregar_elemento_Priorityqueue(Dato, Queue_vieja: queue, Posicion: int):
    Nueva_Queue = queue.Queue()


    if Posicion == 0:
        Nueva_Queue.put(Dato)
        for i in range(Queue_vieja.qsize()): Nueva_Queue.put(Queue_vieja.get())

    else:
        for i in range(Posicion):
            Nueva_Queue.put(Queue_vieja.get())
        Nueva_Queue.put(Dato)
        for i in range(Queue_vieja.qsize()): Nueva_Queue.put(Queue_vieja.get())

    return Nueva_Queue

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

#Creamos el arbol de desición con un nodo inicial y la gráfica del arbol
ARBOL = Arbol()
Arbol_generado = Grafica()

Posiciones_por_agregar = queue.Queue()  # Parametro principal de generar_nodos con direcciones
Profundidad_decision = []   # Guardaremos la distancia entre las hojas y la última desición tomada en una lista
Valor_produndidad =  0       # Cuenta el número de hojas por cada desición
Numero_ramificaciones_disponibles = []

# Generar arbol y dibujar
while True:
    Posiciones_por_agregar_aux = []  # Parametro principal de generar_nodos sin importar su eliminación
    Nodos_por_agregar = []           # Guardar los nodos en una lista para después agregarlos todos al LIFO
    Posicion_Actual = None


    areas_descubiertas[pos_y][pos_x] = True
    Direccion = None

    if ARBOL.Vacio():
        Posicion_inicial = [pos_y, pos_x]
        ARBOL.Agregar_nodo_FIFO(Nodo(pos_y, pos_x))
        ARBOL.Generar_nodos(None)
        Arbol_generado.Agregar_nodo(str(Posicion_inicial))
        Arbol_generado.Generar_Nodos()

    else:
        # 1. ANALISIS DE LOS LADOS
        Areas_Visitadas = sensor_mirar()  # Adquirimos las areas descubiertas
        it = 0

        # 2. FILTRAR LADOS
        # Agregamos los nodos a los que podemos avanzar en un LIFO queue
        for i in range(len(Areas_Visitadas)):

            # almacenamos los nodos a los que solo hay que avanzar
            if matriz[Areas_Visitadas[i].Posicion_y][Areas_Visitadas[i].Posicion_x] == 1:
                if ((Areas_Visitadas[i].Posicion_actual in ARBOL.Nodos_recorridos) is False) or (len(Arbol.Nodos_recorridos) == 0):

                    nodo = Nodo(Areas_Visitadas[i].Posicion_Y, Areas_Visitadas[i].Posicion_X, Areas_Visitadas[i].direccion)

                    Posicion_Actual = ARBOL.Coordenadas_nodo()
                    Direccion = nodo.direccion
                    Nodos_por_agregar.append(nodo)  # ARBOL.Agregar_nodo_LIFO(nodo)

                    if Posiciones_por_agregar.qsize() != 0 and i == 0:
                        Posiciones_por_agregar = Agregar_elemento_Priorityqueue(Direccion, Posiciones_por_agregar, 0)
                        it += 1

                    elif Posiciones_por_agregar.qsize() != 0 and i != 0:
                        Posiciones_por_agregar = Agregar_elemento_Priorityqueue(Direccion, Posiciones_por_agregar, it)
                        it += 1

                    elif Posiciones_por_agregar.qsize() == 0:
                        Posiciones_por_agregar.put(Direccion)
                        it += 1

                    Posiciones_por_agregar_aux.append(Direccion)
                    time.sleep(0.2)




        # Una vez finalizado el analisis de los lados
        else:

            # Contamos el número de ramificaciones mayores a 1 y las contamos
            if len(Posiciones_por_agregar_aux) > 1:
                Numero_ramificaciones_disponibles.append(len(Posiciones_por_agregar_aux) - 1)

            # contamos el número de hojas existentes y las guardamos
            if len(Nodos_por_agregar) > 1:
                Valor_produndidad = 1 if (ARBOL.Numero_Nodos - Valor_produndidad == 0) else ARBOL.Numero_Nodos - Valor_produndidad
                Profundidad_decision.append(Valor_produndidad)
                Valor_produndidad = ARBOL.Numero_Nodos

                for j in range(len(Profundidad_decision)):
                    if (0 in Profundidad_decision) is True:
                        Profundidad_decision.pop(j)


            # De tener al menos un camino a donde ir, procedemos con la creación de nodos
            if len(Nodos_por_agregar) != 0:

                # Coleccionamos en una queue los nodos por agregar
                for i in Nodos_por_agregar:
                    ARBOL.Agregar_nodo_FIFO(i)

                    # Agregamos en la gráfica el valor de los nodos
                    if len(Nodos_por_agregar) == 1:
                        Arbol_generado.Agregar_nodo(str(i.Posicion_actual))
                    else:
                        Arbol_generado.Agregar_ramificacion(str(i.Posicion_actual))

                else:
                    Arbol_generado.Generar_Nodos()

                # Dado las direcciones de cada ramificación, generar nodo
                for i in Posiciones_por_agregar_aux:
                    ARBOL.Generar_nodos(i)

                # Al acabar, ingresar en la lista de direcciones un elemento de las posiciones por agregar
                Direccion = Posiciones_por_agregar.get()
                ARBOL.Agregar_direccion_nodo(Direccion)
                ARBOL.Ingresar_coordenadas(Posicion_Actual)

            # De no tener ninguna posible ramificación
            else:
                Iteracion = Numero_ramificaciones_disponibles[-1]
                Nodos_por_regresar = ARBOL.Numero_Nodos - Valor_produndidad
                Posicion_Actual = ARBOL.Coordenadas_nodo()

                if Iteracion - 1 >= 0:
                    for i in range(Nodos_por_regresar):
                        ARBOL.Eliminar_direccion_nodo()

                    else:
                        ARBOL.Ingresar_coordenadas(Posicion_Actual)  # Ingresamos el nodo ya recorrido
                        ARBOL.Agregar_direccion_nodo(Posiciones_por_agregar.get())  # Asignamos la nueva prioridad
                        Coordenadas = ARBOL.Coordenadas_nodo()
                    pos_y = Coordenadas[0]
                    pos_x = Coordenadas[1]
                    Arbol_generado.Agregar_Padre(str([pos_y, pos_x]))

                    Numero_ramificaciones_disponibles[-1] = Numero_ramificaciones_disponibles[-1] - 1
                    pass


                else:
                    if (pos_x == 14 and pos_y == 1) is False:
                        if Numero_ramificaciones_disponibles[-1] == 0: Numero_ramificaciones_disponibles.pop()

                        for i in range(Nodos_por_regresar):
                            Posicion_Actual = ARBOL.Coordenadas_nodo()
                            ARBOL.Eliminar_direccion_nodo()
                            if (Posicion_Actual in ARBOL.Nodos_recorridos) is False:
                                ARBOL.Ingresar_coordenadas(Posicion_Actual)

                        for i in range(Profundidad_decision.pop()):
                            ARBOL.Eliminar_direccion_nodo()
                        else:
                            ARBOL.Agregar_direccion_nodo(Posiciones_por_agregar.get())
                            Coordenadas = ARBOL.Coordenadas_nodo()
                            pos_y = Coordenadas[0]
                            pos_x = Coordenadas[1]
                        Arbol_generado.Agregar_Padre(str([pos_y, pos_x]))
                        pass

                #Numero_ramificacion = Numero_ramificaciones_disponibles[-1]


                """Regresar posición hasta la última desicion"""
                # ARBOL.Eliminar_direccion_nodo()  Esto solo quita una instrucción

    # De haber llegado a las coordenadas finales, finalizamos el programa
    if pos_x == 14 and pos_y == 1:
        ganado = True
        Arbol_generado.Graficar()

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
    coordenadas = f'Coordenadas: ({pos_y}, {pos_x})'
    texto = fuente.render(coordenadas, True, BLANCO)
    ventana.blit(texto, (10, 10))
    pygame.display.update()

    dibujar_muneco()  # Dibujar el muñeco

    if Direccion == "Arriba":  pos_y -= 1
    if Direccion == "Abajo":   pos_y += 1
    if Direccion == "Derecha": pos_x += 1
    if Direccion == "Izquierda": pos_x -= 1
    Arbol_generado.Agregar_Padre(str([pos_y, pos_x]))

    # Coordenadas de inicio.
    inicio_i = f'In'
    ini_i = fuente.render(inicio_i, True, NEGRO)
    ventana.blit(ini_i, (0, 9 * TAMANO_CUADRO))  # Coordenadas (0, 9) multiplicadas por el tamaño de cuadro

    inicio_f = f'F'
    ini_f = fuente.render(inicio_f, True, NEGRO)
    ventana.blit(ini_f,
                 (14 * TAMANO_CUADRO, 1 * TAMANO_CUADRO))  # Coordenadas (14, 1) multiplicadas por el tamaño de cuadro

    pygame.display.update()


