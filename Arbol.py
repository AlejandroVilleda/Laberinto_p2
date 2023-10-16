import queue
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp

# Creación de la estructura de datos del arbol
class Nodo:

    # Valorres iniciales del nodo
    def __init__(self, Posicion_y = None, Posicion_x = None, Direccion = None, Arriba = None, Abajo = None, Izquierda = None, Derecha = None):
        self.Posicion_y = Posicion_y
        self.Posicion_x = Posicion_x
        self.Direccion = Direccion
        self.Arriba = Arriba
        self.Abajo = Abajo
        self.Derecha = Derecha
        self.Izquierda = Izquierda

    @property  # Dirección que toma el nood
    def direccion(self): return self.Direccion

    @property  # Posición en la que se ubica el nodo en el laberinto
    def Posicion_actual(self):  return [self.Posicion_y, self.Posicion_x]

    @property # Posición X
    def Posicion_X(self): return self.Posicion_x

    @property # Posición Y
    def Posicion_Y(self): return self.Posicion_y


# Creación del Arbol
class Arbol:

    # Variables de la clase
    Nodos_por_agregar = queue.Queue()  # Cola de prioridad para insertar nodos al arbol
    Nodos_visitados: list = []      # Lista de nodos ya recorridos en el arbol
    Direcciones_generadas: list = []       # Lista de direcciones para llegar a la hoja

    # Inicio del arbol vacio
    def __init__(self): self.Inicio = None

    def Generar_nodos(self, Direccion):

        # Si esta vacio el arbol
        if self.Vacio() == True:
            Nuevo_Nodo: Nodo = Arbol.Nodos_por_agregar.get()  # Obtenemos el único nodo que debe existir en el queue
            self.Inicio = Nuevo_Nodo    # Lo ingresamos como inicio del arbol

            # Arbol.Nodos_visitados.append(Nuevo_Nodo.Posicion_actual)  # Colocamos la posición del nodo como recorrido

        # si no esta vacio
        else:
            # Evaluamos las direcciones en las que debemos desarrollar el arbol
            if Direccion == "Arriba":
                aux = self.Inicio

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in Arbol.Direcciones_generadas:
                    if i == 'Arriba': aux = aux.Arriba
                    if i == 'Abajo': aux = aux.Abajo
                    if i == 'Derecha': aux = aux.Derecha
                    if i == 'Izquierda': aux = aux.Izquierda

                Nuevo_nodo: Nodo = Arbol.Nodos_por_agregar.get()
                aux.Arriba = Nuevo_nodo
                #Arbol.Nodos_visitados.append(Nuevo_nodo.Posicion_actual)

            if Direccion == "Abajo":
                aux = self.Inicio

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in Arbol.Direcciones_generadas:
                    if i == 'Arriba': aux = aux.Arriba
                    if i == 'Abajo': aux = aux.Abajo
                    if i == 'Derecha': aux = aux.Derecha
                    if i == 'Izquierda': aux = aux.Izquierda

                Nuevo_nodo: Nodo = Arbol.Nodos_por_agregar.get()
                aux.Abajo = Nuevo_nodo
                #Arbol.Nodos_visitados.append(Nuevo_nodo.Posicion_actual)

            if Direccion == "Derecha":
                aux = self.Inicio

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in Arbol.Direcciones_generadas:
                    if i == 'Arriba': aux = aux.Arriba
                    if i == 'Abajo': aux = aux.Abajo
                    if i == 'Derecha': aux = aux.Derecha
                    if i == 'Izquierda': aux = aux.Izquierda

                Nuevo_nodo: Nodo = Arbol.Nodos_por_agregar.get()
                aux.Derecha = Nuevo_nodo
                #Arbol.Nodos_visitados.append(Nuevo_nodo.Posicion_actual)

            if Direccion == "Izquierda":
                aux = self.Inicio

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in Arbol.Direcciones_generadas:
                    if i == 'Arriba': aux = aux.Arriba
                    if i == 'Abajo': aux = aux.Abajo
                    if i == 'Derecha': aux = aux.Derecha
                    if i == 'Izquierda': aux = aux.Izquierda

                Nuevo_nodo: Nodo = Arbol.Nodos_por_agregar.get()
                aux.Izquierda = Nuevo_nodo
                #Arbol.Nodos_visitados.append(Nuevo_nodo.Posicion_actual)

            pass



    # Agregamos los nodos a una queue para posteriormente ingresarlos en el arbol
    def Agregar_nodo_FIFO(self, nodo): self.Nodos_por_agregar.put(nodo)

    # Agregamos la dirección o ruta que debe seguir el arbol para ingresar el nodo
    def Agregar_direccion(self, direccion): self.Direcciones_generadas.append(direccion)

    # Eliminamos la últma ruta que debe seguir el arbol
    def Eliminar_direccion_nodo(self): self.Direcciones_generadas.pop()

    # Contamos el número de hojas en toda la ramificación del arbol
    @property
    def Numero_Nodos(self): return len(self.Direcciones_generadas)

    # Verifica que el arbol esté vacio
    def Vacio(self): return self.Inicio == None

    # Insertar la posición ya recorrida
    def Agregar_posicion(self, Posicion): self.Nodos_visitados.append(Posicion)

    # Obtenemos las coordenadas del nodo actual
    def Coordenadas_nodo(self):
        aux: Nodo = self.Inicio

        # Llegamos a la hoja siguiendo las respectivas desiciones generadas
        for i in Arbol.Direcciones_generadas:
            if i == 'Arriba': aux = aux.Arriba
            if i == 'Abajo': aux = aux.Abajo
            if i == 'Derecha': aux = aux.Derecha
            if i == 'Izquierda': aux = aux.Izquierda
        else: return aux.Posicion_actual


class Grafica:

    # Nodos recorridos y por graficar
    Nodos = []
    Nodos_Ramificados = []
    Padre = None
    i = 1

    def __init__(self): self.tree = nx.DiGraph()

    # Agregar nodos para graficar
    def Agregar_nodo(self, Coordenadas):
        Grafica.Nodos.append(Coordenadas)

        # Asignando valores al padre del nodo
        if (len(self.Nodos) > 1) and Grafica.i == 1:
                self.Padre = None
        else:
            if self.Padre == None: self.Padre = self.Nodos[0]

            """
                    if (len(self.Nodos) > 1) and Grafica.i == 1:
                            self.Padre = None
                    elif (len(self.Nodos) == 1) and Grafica.i >= 1:
                        if self.Padre == None: self.Padre = self.Nodos[0]
            """

    # Agregamos nodos que corresponda a ramificaciones mayores a 1
    def Agregar_ramificacion(self, Coordenadas):
        self.Padre = self.Nodos[-1]

        Grafica.Nodos_Ramificados.append(Coordenadas)

    # De las funciones anteriores, ingresamos los nodos al arbol
    def Generar_Nodos(self):
        It = Grafica.i
        # Agregando al nodo
        for Grafica.i in range(len(self.Nodos)):
            self.tree.add_node(self.Nodos[Grafica.i])

        # Uniendo los nodos
        if len(self.Nodos) > 1 and Grafica.i != 0:  # MODIFICAR I = 1
            T = len(self.Nodos)
            for It in range(Grafica.i, T):
                if It - 1 != -1:
                    self.tree.add_edge(self.Nodos[It - 1], self.Nodos[It])

        # Unimos las ramificaciones mediante el padre
        if len(self.Nodos) == 1 and Grafica.i != 1:
            T = len(self.Nodos)
            for It in range(Grafica.i, T):
                self.tree.add_edge(self.Padre, self.Nodos[It])

        # Agregando nodos hijos
        if len(Grafica.Nodos_Ramificados) != 0:
            for k in range(len(self.Nodos_Ramificados)):
                self.tree.add_node(self.Nodos_Ramificados[k])

            # Uniendo los nodos ramificados
            for k in range(len(self.Nodos_Ramificados)):
                self.tree.add_edge(self.Padre, self.Nodos_Ramificados[k])
            else:
                Grafica.Nodos.clear()

        Grafica.Nodos_Ramificados.clear()
        Grafica.i += 1
        pass

    def Agregar_Padre(self, Posicion):
        self.Padre = Posicion
    def Graficar(self):
        tree = self.tree
        pos = nx.kamada_kawai_layout(tree, scale=1)

        # Dibujar el árbol
        plt.figure(figsize=(4, 8))  # Tamaño de la figura
        nx.draw(tree, pos, with_labels=True, node_size=400, node_color='lightblue', font_size=8, arrows=False)
        # Centrar el árbol en la figura
        plt.margins(0.2, 0.1)
        plt.axis('off')  # Ocultar ejes

        plt.show()