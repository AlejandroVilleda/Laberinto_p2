import pygame
import sys
import time
from Arbol import *

"""
FUNCIONES PRINCIPALES___________________________________________________"""
# Función que dibuja al meñeco
def dibujar_muneco(): ventana.blit(muneco_img, (pos_x * TAMANO_CUADRO, pos_y * TAMANO_CUADRO))

# Devuelve una lista de objetos Nodos con las principales caracteristicas que necesitamos (posición y dirección)
def sensor_mirar(Orden: list):
    areas_descubiertas[pos_y][pos_x] = True  # Mostramos el área en el que nos encontramos
    Lista_areas_descubiertas = [None]        # Guardamos aquí una lista de las áreas descubiertas
    Lista_Auxiliar = [None]                  # Almacena la posición de las áreas

    # Revisamos el elemento de ARRIBA
    if pos_y - 1 >= 0:
        areas_descubiertas[pos_y - 1][pos_x] = True
        Lista_Auxiliar = Nodo(pos_y - 1, pos_x, 'Arriba')
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    # Revisamos el elemento de ABAJO
    if pos_y + 1 < len(matriz):
        areas_descubiertas[pos_y + 1][pos_x] = True
        Lista_Auxiliar = Nodo(pos_y + 1, pos_x, 'Abajo')
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    # Revisamos el elemento de la DERECHA
    if pos_x + 1 < len(matriz[0]):
        areas_descubiertas[pos_y][pos_x + 1] = True
        Lista_Auxiliar = Nodo(pos_y, pos_x + 1, 'Derecha')
        Lista_areas_descubiertas.append(Lista_Auxiliar)


    # Revisamos el elemento de la IZQUIERDA
    if pos_x - 1 >= 0:
        areas_descubiertas[pos_y][pos_x - 1] = True
        Lista_Auxiliar = Nodo(pos_y, pos_x - 1, 'Izquierda')
        Lista_areas_descubiertas.append(Lista_Auxiliar)

    areas_visitadas[pos_y][pos_x] = True

    # Eliminamos aquellos valores en la lista con valores nulos
    Lista_Auxiliar_2 = []

    # Recorremos la lista de áreas visitadas en busqueda de iteraciones vacias
    for i in range(len(Lista_areas_descubiertas)):
        if Lista_areas_descubiertas[i] == None:
            Lista_Auxiliar_2.append(i)  # Almacenamos su posición en una lista extra

    else:  # Eliminamos esos elementos que no nos sirvan
        for i in range(len(Lista_Auxiliar_2)):
            Lista_areas_descubiertas.pop(i)
            Lista_Auxiliar_2.pop()
            i -= 1

            if i + 1 == len(Lista_Auxiliar_2) or len(Lista_Auxiliar_2) == 0: break   # condición para romper ciclo

    Nueva_Lista = []  # Almacenamos en él la lista ordenada


    # Algoritmo para ordenar la lista
    for i in Orden:
        for j in Lista_areas_descubiertas:
            if i in j.direccion:
                Nueva_Lista.append(j)


    return Nueva_Lista






# Devuelve un queue FIFO. Almacena las direcciones de las posibles ramificaciones a tomar bajo el criterio de prioridad
def Agregar_elemento_Priorityqueue(Dato, Queue_vieja: queue, Posicion: int):
    Nueva_Queue = queue.Queue()

    # Algoritmo de insersión de datos de una FIFO QUEUE en una posición N
    if Posicion == 0:
        Nueva_Queue.put(Dato)
        for i in range(Queue_vieja.qsize()): Nueva_Queue.put(Queue_vieja.get())

    else:
        for i in range(Posicion): Nueva_Queue.put(Queue_vieja.get())
        Nueva_Queue.put(Dato)
        for i in range(Queue_vieja.qsize()): Nueva_Queue.put(Queue_vieja.get())

    return Nueva_Queue


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

# Coordenadas iniciales del muñequito.
pos_x = 0
pos_y = 9
pos_x_inicio = pos_x
pos_y_inicio = pos_y
pos_x_final = 4
pos_y_final = 6
# x = 4, y = 6
# x = 14, y = 1

Orden = ['Arriba', 'Abajo', 'Derecha', 'Izquierda']  # Orden de prioridad

# 0: Profundidad
# 1: Anchura
Algoritmo = 1

"""
GENERAR MATRIZ__________________________________________________________"""

# Abre el archivo .txt que contiene la matriz. La leemos y almacenamos
with open('./Laberinto.txt', 'r') as f: lineas = f.readlines()

# Iterar a través de las líneas leidas y crear una lista de listas (matriz)
for linea in lineas:
    fila = [int(valor) for valor in linea.strip().split(',')]
    matriz.append(fila)

# Dimensiones de la ventana
ANCHO = len(matriz[0]) * TAMANO_CUADRO
ALTO = len(matriz) * TAMANO_CUADRO

"""
INICIALIZAR PYGAME Y CARGAR VALORES_____________________________________"""
pygame.init()   # Inicializar pygame

# Crear ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))    # Generar ventana
pygame.display.set_caption("Laberinto")             # Nombre de la ventana

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

Ramificaciones_por_seguir = queue.Queue()  # Almacena la dirección de las ramificaciones a seguir bajo el criterio de prioridad
Profundidad_inicial =  0                   # Almacena la profundidad del último nodo padre recorrido
Profundidades = []                         # Almacena las profundidades entre cada nodo padre
Numero_ramificaciones_disponibles = []     # Almacena el número de nodos disponibles por recorrer




# Inicialización del algoritmo
if Algoritmo == 0:
    # algoritmo de profundidad
    while True:

        # estas listas y variable se reiniciarán al comenzar un nuevo ciclo
        Direcciones_por_agregar = []     # Almacena las direcciones a agregar al arbol bajo el orden de prioridad
        Nodos_por_agregar = []      # Almacena los nodos a agregar al arbol bajo el orden de prioridad
        Posicion_Actual = None      # Almacena la posición en la que nos encontramos en cada iteración
        Direccion = None            # Almacena la dirección que vamos a agregar al nodo
        areas_descubiertas[pos_y][pos_x] = True

        # PASO 1. CREAR EL NODO RAÍZ. Solo ocurre en la primera iteración
        if ARBOL.Vacio():

            # Dibujar el laberinto
            dibujar_muneco()
            for fila in range(len(matriz)):
                for columna in range(len(matriz[0])):
                    if not areas_descubiertas[fila][columna]:
                        color = GRIS  # Si no se ha descubierto, pintar de gris

                    else:
                        color = BLANCO if matriz[fila][columna] == 1 else NEGRO

                    pygame.draw.rect(ventana, color,
                                     (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                    if areas_visitadas[fila][columna]:
                        letra_v_rect = letra_v.get_rect()
                        letra_v_rect.topleft = (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO)
                        ventana.blit(letra_v, letra_v_rect)
            pygame.display.update()

            # Creamos un objeto nodo con posición inicial y sin dirección en el arbol
            Posicion_inicial = [pos_y, pos_x]
            ARBOL.Agregar_nodo_FIFO(Nodo(pos_y, pos_x))
            ARBOL.Generar_nodos(None)

            # Agregamos la posición inicial al arbol de graficación
            Arbol_generado.Agregar_nodo(str(Posicion_inicial))
            Arbol_generado.Generar_Nodos()
            continue # Saltamos directamente a la siguiente iteración

        # PASO 2. ANÁLISIS DE LADOS DEL NODO. Conocemos las posiciones y direcciones de los elementos al rededor del punto
        Areas_Visitadas = sensor_mirar(Orden)  # Adquirimos las áreas al rededor del punto
        it = 0      # Cuenta el número de direcciones a recorrer en la Queue

        # PASO 3. FILTRAR LADOS. Registramos los datos de las áreas a las que podemos desplazarnos
        # Iteramos cada lado visitado
        for i in range(len(Areas_Visitadas)):

            # Si el área visitado es blanco y no lo hemos recorrido antes, registramos su posición y dirección
            if matriz[Areas_Visitadas[i].Posicion_y][Areas_Visitadas[i].Posicion_x] == 1:
                if (Areas_Visitadas[i].Posicion_actual in ARBOL.Nodos_visitados) is False:

                    # Almacenamos el nodo iterado y lo almacenamos para agregar al arbol
                    nodo = Nodo(Areas_Visitadas[i].Posicion_Y, Areas_Visitadas[i].Posicion_X, Areas_Visitadas[i].direccion)
                    Nodos_por_agregar.append(nodo)
                    Posicion_Actual = ARBOL.Coordenadas_nodo()

                    # Almacenamos dirección del nodo iterado y lo almacenamos para utilizarlo como dato iterador
                    Direccion = nodo.direccion
                    Direcciones_por_agregar.append(Direccion)

                    # Algoritmo para almacenar direcciones al Queue
                    if Ramificaciones_por_seguir.qsize() == 0:
                        Ramificaciones_por_seguir.put(Direccion)
                        it += 1

                    else:
                        Ramificaciones_por_seguir = Agregar_elemento_Priorityqueue(Direccion, Ramificaciones_por_seguir, it)
                        it += 1

        # PASO 4. INSERTAR DATOS AL ÁRBOL
        else:

            # Almacenamos el número de nodos disponibles a ingresar (N - 1). Eliminamos uno porque ya lo recorreremos
            if len(Nodos_por_agregar) > 1:
                Numero_ramificaciones_disponibles.append(len(Direcciones_por_agregar) - 1)

                # Almacenamos la profundidad entre la hoja actual y el nodo padre
                Profundidad_inicial = ARBOL.Numero_Nodos - Profundidad_inicial  # Profundidad final - Profundidad inicial
                Profundidades.append(Profundidad_inicial)   # Almacenamos
                Profundidad_inicial = ARBOL.Numero_Nodos    # actualizamos la profundidad inicial

            # De tener al menos un camino a donde ir, procedemos con la creación de nodos en el arbol
            if len(Nodos_por_agregar) != 0:

                # Coleccionamos en una queue los nodos por agregar
                for i in Nodos_por_agregar:
                    ARBOL.Agregar_nodo_FIFO(i)

                    # Agregamos en la gráfica el valor de los nodos
                    if len(Nodos_por_agregar) == 1:
                        Arbol_generado.Agregar_nodo(str(i.Posicion_actual))
                    else:
                        Arbol_generado.Agregar_ramificacion(str(i.Posicion_actual))

                else: Arbol_generado.Generar_Nodos()  # generamos los nodos al arbo, de graficación

                # Dado las direcciones de cada ramificación, generar nodo en el arbol
                for i in Direcciones_por_agregar:
                    ARBOL.Generar_nodos(i)

                # Retiramos la dirección registrada previamente y la registramos en el arbol junto con la posición -------------------POSIBLE SELECCION DE PRIORIDAD
                Direccion = Ramificaciones_por_seguir.get()
                ARBOL.Agregar_direccion(Direccion)
                ARBOL.Agregar_posicion(Posicion_Actual)

            # PASO 5. GENERAR RAMIFICACIONES
            # De no tener ninguna ramificación
            else:
                Posicion_Actual = ARBOL.Coordenadas_nodo()
                Iteracion = Numero_ramificaciones_disponibles[-1]  # Almacenamos el número de ramas disponibles a tomar
                Nodos_por_regresar = ARBOL.Numero_Nodos - Profundidad_inicial   # Regresamos N números hasta el nodo padre

                # Si tenemos ramificaciones disponibles en el nodo, tomamos la otra ramificación más proxima
                if Iteracion - 1 >= 0:
                    for i in range(Nodos_por_regresar): ARBOL.Eliminar_direccion_nodo()  # Eliminamos la dirección a seguir

                    ARBOL.Agregar_direccion(Ramificaciones_por_seguir.get())  # Asignamos el siguiente valor de la prioridad
                    ARBOL.Agregar_posicion(Posicion_Actual)  # Registramos el nodo anterior como recorrido

                    # Obtenemos la posición actual y la tomamos
                    Coordenadas = ARBOL.Coordenadas_nodo()
                    pos_y = Coordenadas[0]
                    pos_x = Coordenadas[1]
                    Arbol_generado.Agregar_Padre(str([pos_y, pos_x])) # almacenamos al nuevo padre a graficar
                    Arbol_generado.Resetear()   # Forzamos a un reseteo debido a un cambio de ramificación
                    Numero_ramificaciones_disponibles[-1] -= 1  # Restamos una rama ya que ya la acabamos de tomar
                    pass

                # Si ya no tenemos ramificaciones disponibles
                else:
                    # Si no hemos llegado al destino
                    if (pos_x == pos_x_final and pos_y == pos_y_final) is False:

                        # Realizamos esto hasta que cambiemos de ramificación
                        while(Numero_ramificaciones_disponibles[-1] == 0):

                            # eliminamos todos los valores 0 en las ramificaciones existentes
                            Numero_ramificaciones_disponibles.pop()

                            # Eliminamos los nodos hijos hasta el último nodo padre
                            for i in range(Nodos_por_regresar):
                                Posicion_Actual = ARBOL.Coordenadas_nodo()
                                ARBOL.Eliminar_direccion_nodo()

                                # Almacenamos la posición actual como recorrido en caso de no estarlo
                                if (Posicion_Actual in ARBOL.Nodos_visitados) is False: ARBOL.Agregar_posicion(Posicion_Actual)

                            # regresamos a la última desición tomada
                            for i in range(Profundidades.pop()): ARBOL.Eliminar_direccion_nodo()

                            # Actualiando el valor de la profundidad inicial
                            aux_p = 0
                            for u in Profundidades:
                                aux_p = u + aux_p
                            else:
                                Profundidad_inicial = aux_p
                            Nodos_por_regresar = ARBOL.Numero_Nodos - Profundidad_inicial
                            pass

                        # Tomamos la siguiente ramificación bajo el criterio de prioridad y obtenemos la posición actual
                        else:
                            ARBOL.Agregar_direccion(Ramificaciones_por_seguir.get())
                            Coordenadas = ARBOL.Coordenadas_nodo()
                            pos_y = Coordenadas[0]
                            pos_x = Coordenadas[1]
                        Arbol_generado.Agregar_Padre(str([pos_y, pos_x]))
                        Arbol_generado.Resetear()   # Forzamos a un reseteo debido a un cambio de ramificación
                        Numero_ramificaciones_disponibles[-1] -= 1  # restamos la ramificación disponible

                        # Actualiando el valor de la profundidad inicial
                        aux_p = 0
                        for u in Profundidades: aux_p = u + aux_p
                        else: Profundidad_inicial = aux_p
                        Nodos_por_regresar = ARBOL.Numero_Nodos - Profundidad_inicial
                        pass


        time.sleep(0.2)

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
        Arbol_generado.Agregar_Padre(str([pos_y, pos_x]))

        # Coordenadas de inicio.
        inicio_i = f'In'
        ini_i = fuente.render(inicio_i, True, NEGRO)
        ventana.blit(ini_i, (pos_x_inicio, pos_y_inicio * TAMANO_CUADRO))  # Coordenadas (0, 9) multiplicadas por el tamaño de cuadro

        inicio_f = f'F'
        ini_f = fuente.render(inicio_f, True, NEGRO)
        ventana.blit(ini_f,
                     (pos_x_final * TAMANO_CUADRO, pos_y_final * TAMANO_CUADRO))  # Coordenadas (14, 1) multiplicadas por el tamaño de cuadro

        pygame.display.update()

        # De haber llegado a las coordenadas finales, finalizamos el programa
        if pos_x == pos_x_final and pos_y == pos_y_final:
            # Dibujar el laberinto
            for fila in range(len(matriz)):
                for columna in range(len(matriz[0])):
                    if not areas_descubiertas[fila][columna]:
                        color = GRIS  # Si no se ha descubierto, pintar de gris

                    else:
                        color = BLANCO if matriz[fila][columna] == 1 else NEGRO

                    pygame.draw.rect(ventana, color,
                                     (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                    if areas_visitadas[fila][columna]:
                        letra_v_rect = letra_v.get_rect()
                        letra_v_rect.topleft = (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO)
                        ventana.blit(letra_v, letra_v_rect)

            dibujar_muneco()  # Dibujar el muñeco
            #pygame.display.update()
            ganado = True

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
            Arbol_generado.Graficar()
            pygame.time.delay(3000)  # Espera 3 segundos
            pygame.quit()
            sys.exit()

# Para el algoritmo de anchura
else:

    Ramificaciones_por_seguir = []  # Lista que almacena un conjunto de direcciones por seguir

    # algoritmo de anchura
    while True:

        # estas listas y variable se reiniciarán al comenzar un nuevo ciclo
        Direcciones_por_agregar = []     # Almacena las direcciones a agregar al arbol bajo el orden de prioridad
        Nodos_por_agregar = []      # Almacena los nodos a agregar al arbol bajo el orden de prioridad
        Posicion_Actual = None      # Almacena la posición en la que nos encontramos en cada iteración
        Direccion = None            # Almacena la dirección que vamos a agregar al nodo
        areas_descubiertas[pos_y][pos_x] = True

        # PASO 1. CREAR EL NODO RAÍZ. Solo ocurre en la primera iteración
        if ARBOL.Vacio():

            # Dibujar el laberinto
            dibujar_muneco()
            for fila in range(len(matriz)):
                for columna in range(len(matriz[0])):
                    if not areas_descubiertas[fila][columna]:
                        color = GRIS  # Si no se ha descubierto, pintar de gris

                    else:
                        color = BLANCO if matriz[fila][columna] == 1 else NEGRO

                    pygame.draw.rect(ventana, color,
                                     (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                    if areas_visitadas[fila][columna]:
                        letra_v_rect = letra_v.get_rect()
                        letra_v_rect.topleft = (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO)
                        ventana.blit(letra_v, letra_v_rect)
            pygame.display.update()

            # Creamos un objeto nodo con posición inicial y sin dirección en el arbol
            Posicion_inicial = [pos_y, pos_x]
            ARBOL.Agregar_nodo_FIFO(Nodo(pos_y, pos_x))
            ARBOL.Generar_nodos(None)

            # Agregamos la posición inicial al arbol de graficación
            Arbol_generado.Agregar_nodo(str(Posicion_inicial))
            Arbol_generado.Generar_Nodos()
            continue # Saltamos directamente a la siguiente iteración

        # PASO 2. ANÁLISIS DE LADOS DEL NODO. Conocemos las posiciones y direcciones de los elementos al rededor del punto
        # Comienzo
        if len(Ramificaciones_por_seguir) == 0:
            Areas_Visitadas = sensor_mirar(Orden)  # Adquirimos las áreas al rededor del punto

            # PASO 3. FILTRAR LADOS. Registramos los datos de las áreas a las que podemos desplazarnos
            # Iteramos cada lado visitado
            for i in range(len(Areas_Visitadas)):

                # Si el área visitado es blanco y no lo hemos recorrido antes, registramos su posición y dirección
                if matriz[Areas_Visitadas[i].Posicion_y][Areas_Visitadas[i].Posicion_x] == 1:
                    if (Areas_Visitadas[i].Posicion_actual in ARBOL.Nodos_visitados) is False:

                        # Almacenamos el nodo iterado y lo almacenamos para agregar al arbol
                        Nuevo_nodo = Nodo(Areas_Visitadas[i].Posicion_Y, Areas_Visitadas[i].Posicion_X, Areas_Visitadas[i].direccion)
                        Nodos_por_agregar.append(Nuevo_nodo)
                        Posicion_Actual = ARBOL.Coordenadas_nodo()

                        # Almacenamos dirección del nodo iterado y lo almacenamos para utilizarlo como dato iterador
                        Direccion = Nuevo_nodo.direccion
                        Direcciones_por_agregar.append(Direccion)

            # PASO 4. INSERTAR DATOS AL ÁRBOL
            else:

                # De tener al menos un camino a donde ir, procedemos con la creación de nodos en el arbol
                if len(Nodos_por_agregar) != 0:

                    # Coleccionamos en una queue los nodos por agregar
                    for i in Nodos_por_agregar:
                        ARBOL.Agregar_nodo_FIFO(i)

                        # Agregamos en la gráfica el valor de los nodos
                        #if len(Nodos_por_agregar) == 1:
                         #   Arbol_generado.Agregar_nodo(str(i.Posicion_actual))
                        #else:
                         #   Arbol_generado.Agregar_ramificacion(str(i.Posicion_actual))

                    else:
                        #Arbol_generado.Generar_Nodos()  # generamos los nodos al arbo, de graficación
                        pass

                    # Dado las direcciones de cada ramificación, generar nodo en el arbol
                    for i in Direcciones_por_agregar:
                        ARBOL.Generar_nodos(i)

                    # Retiramos la dirección registrada previamente y la registramos en el arbol junto con la posición -------------------POSIBLE SELECCION DE PRIORIDAD
                    Ramificaciones_por_seguir.append(Direcciones_por_agregar)

                    ARBOL.Agregar_direccion(Direccion)
                    ARBOL.Agregar_posicion(Posicion_Actual)

        else:
            for Ramificacion in Ramificaciones_por_seguir:

                # Agregamos el conjunto de direcciones actuales
                ARBOL.Eliminar_direccion()
                ARBOL.Agregar_ramificacion(Ramificacion)
                Posicion_Actual = ARBOL.Coordenadas_nodo()

                Areas_Visitadas = sensor_mirar(Orden)  # Adquirimos las áreas al rededor del punto

                # PASO 3. FILTRAR LADOS. Registramos los datos de las áreas a las que podemos desplazarnos
                # Iteramos cada lado visitado
                for i in range(len(Areas_Visitadas)):

                    # Si el área visitado es blanco y no lo hemos recorrido antes, registramos su posición y dirección
                    if matriz[Areas_Visitadas[i].Posicion_y][Areas_Visitadas[i].Posicion_x] == 1:
                        if (Areas_Visitadas[i].Posicion_actual in ARBOL.Nodos_visitados) is False:
                            # Almacenamos el nodo iterado y lo almacenamos para agregar al arbol
                            Nuevo_nodo = Nodo(Areas_Visitadas[i].Posicion_Y, Areas_Visitadas[i].Posicion_X, Areas_Visitadas[i].direccion)
                            Nodos_por_agregar.append(Nuevo_nodo)
                            Posicion_Actual = ARBOL.Coordenadas_nodo()

                            # Almacenamos dirección del nodo iterado y lo almacenamos para utilizarlo como dato iterador
                            Direccion = Nuevo_nodo.direccion
                            Direcciones_por_agregar.append(Direccion)

                # PASO 4. INSERTAR DATOS AL ÁRBOL
                else:

                    # De tener al menos un camino a donde ir, procedemos con la creación de nodos en el arbol
                    if len(Nodos_por_agregar) == 1:

                        # Coleccionamos en una queue los nodos por agregar
                        for i in Nodos_por_agregar:
                            ARBOL.Agregar_nodo_FIFO(i)

                            # Agregamos en la gráfica el valor de los nodos
                            # if len(Nodos_por_agregar) == 1:
                            #   Arbol_generado.Agregar_nodo(str(i.Posicion_actual))
                            # else:
                            #   Arbol_generado.Agregar_ramificacion(str(i.Posicion_actual))

                        else:
                            # Arbol_generado.Generar_Nodos()  # generamos los nodos al arbo, de graficación
                            pass

                        # Dado las direcciones de cada ramificación, generar nodo en el arbol
                        for i in Direcciones_por_agregar:
                            ARBOL.Generar_nodos(i)

                        # Retiramos la dirección registrada previamente y la registramos en el arbol junto con la posición -------------------POSIBLE SELECCION DE PRIORIDAD
                        #Ramificaciones_por_seguir.append(Direcciones_por_agregar)
                        Ramificacion.append(Direcciones_por_agregar[0])



                        ARBOL.Agregar_direccion(Direccion)
                        ARBOL.Agregar_posicion(Posicion_Actual)

                pass

        time.sleep(0.2)

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
        Arbol_generado.Agregar_Padre(str([pos_y, pos_x]))

        # Coordenadas de inicio.
        inicio_i = f'In'
        ini_i = fuente.render(inicio_i, True, NEGRO)
        ventana.blit(ini_i, (pos_x_inicio, pos_y_inicio * TAMANO_CUADRO))  # Coordenadas (0, 9) multiplicadas por el tamaño de cuadro

        inicio_f = f'F'
        ini_f = fuente.render(inicio_f, True, NEGRO)
        ventana.blit(ini_f,
                     (pos_x_final * TAMANO_CUADRO, pos_y_final * TAMANO_CUADRO))  # Coordenadas (14, 1) multiplicadas por el tamaño de cuadro

        pygame.display.update()

        # De haber llegado a las coordenadas finales, finalizamos el programa
        if pos_x == pos_x_final and pos_y == pos_y_final:
            # Dibujar el laberinto
            for fila in range(len(matriz)):
                for columna in range(len(matriz[0])):
                    if not areas_descubiertas[fila][columna]:
                        color = GRIS  # Si no se ha descubierto, pintar de gris

                    else:
                        color = BLANCO if matriz[fila][columna] == 1 else NEGRO

                    pygame.draw.rect(ventana, color,
                                     (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO))
                    if areas_visitadas[fila][columna]:
                        letra_v_rect = letra_v.get_rect()
                        letra_v_rect.topleft = (columna * TAMANO_CUADRO, fila * TAMANO_CUADRO)
                        ventana.blit(letra_v, letra_v_rect)

            dibujar_muneco()  # Dibujar el muñeco
            #pygame.display.update()
            ganado = True

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
            Arbol_generado.Graficar()
            pygame.time.delay(3000)  # Espera 3 segundos
            pygame.quit()
            sys.exit()
