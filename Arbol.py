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

    def __call__(self, Posicion_y = None, Posicion_x = None, Direccion = None, Arriba = None, Abajo = None, Izquierda = None, Derecha = None):
        self.Posicion_y = Posicion_y
        self.Posicion_x = Posicion_x
        self.Direccion = Direccion
        self.Arriba = Arriba
        self.Abajo = Abajo
        self.Derecha = Derecha
        self.Izquierda = Izquierda
        return Nodo(Posicion_y, Posicion_x, Direccion)

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
            pass



    # Agregamos los nodos a una queue para posteriormente ingresarlos en el arbol
    def Agregar_nodo_FIFO(self, nodo): self.Nodos_por_agregar.put(nodo)

    # Agregamos la dirección o ruta que debe seguir el arbol para ingresar el nodo
    def Agregar_direccion(self, direccion): self.Direcciones_generadas.append(direccion)

    # Agregamos una ramificación particular
    def Agregar_ramificacion(self, Direccion: list): Arbol.Direcciones_generadas = Direccion.copy()

    # Eliminamos la últma ruta que debe seguir el arbol
    def Eliminar_direccion_nodo(self): self.Direcciones_generadas.pop()

    # Eliminamos la ramificación en su totalidad
    def Eliminar_direccion(self): self.Direcciones_generadas.clear()

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
    i = 0

    def __init__(self): self.tree = nx.DiGraph()

    # Agregar nodos a una lista para agregarlos al arbol después
    def Agregar_nodo(self, Coordenadas):

        # Asignando valores al padre del nodo
        if self.tree.size() == 0: self.Padre = None         # Caso inicial: t(0)
        elif self.Padre == None: self.Padre = self.Nodos[0] # Caso Inicial + 1:  t(1)

        Grafica.Nodos.append(Coordenadas)


    # Agregamos hijos de un nodo hoja a una lista para agregarlos al arbol después
    def Agregar_ramificacion(self, Coordenadas):
        self.Padre = self.Nodos[-1] # el padre será el nodo hoja
        Grafica.Nodos_Ramificados.append(Coordenadas)


    # Almacenar nodos al arbol
    def Generar_Nodos(self):
        It = Grafica.i  # Iterador

        # Agregamos los nodos dentro del arbol
        for x in range(Grafica.i, len(self.Nodos)): self.tree.add_node(self.Nodos[x])

        # Unimos los elementos siempre que existan más de un nodo almacenado
        #Requerimos mínimo 2 elementos para comenzar a unificarlos
        if len(self.Nodos) > 1 and Grafica.i >= 1:
            # Unimos nodos como: [Padre] -- [n] -- [n + 1] -- [n + 2]
            for x in range(Grafica.i, len(self.Nodos)): self.tree.add_edge(self.Nodos[x - 1], self.Nodos[x])

        # Unimos los nuevos elementos al padre proveniente de una ramificación, generando otra ramificación
        if (len(self.Nodos) == 1 and It > 1) or (len(self.Nodos) == 1 and self.tree.size() > 1) and (len(self.Nodos_Ramificados) == 0): # CHECAR PQ NO ESTA BIEN________________________________
            for x in range(Grafica.i, len(self.Nodos)):
                if self.Padre != self.Nodos[x]: self.tree.add_edge(self.Padre, self.Nodos[x])

        # Agregando los hijos de un nodo siemrpe que existan
        if len(Grafica.Nodos_Ramificados) != 0:
            for k in range(len(self.Nodos_Ramificados)): self.tree.add_node(self.Nodos_Ramificados[k])

            # Uniendo los nodos ramificados con su respectivo padre
            for k in range(len(self.Nodos_Ramificados)): self.tree.add_edge(self.Padre, self.Nodos_Ramificados[k])

            else: # al finalizar limpiamos los datos y reseteamos el iterador
                Grafica.Nodos.clear()
                Grafica.i = -1

        Grafica.Nodos_Ramificados.clear()
        Grafica.i += 1  # Avanzamos una posición al siguiente nodo
        pass

    # Actualiza el valor del padre en caso de saltos en el arbol
    def Agregar_Padre(self, Posicion):
        self.Padre = Posicion

    # Devuelve el valor del padre
    @property
    def Valor_padre(self): return self.Padre

    # Forzamos un reseteo de datos en caso de saltos en el arbol
    def Resetear(self):
        self.Nodos.clear()
        Grafica.i = 0

    # Generamos la gráfica del arbol en una ventana
    def Graficar(self):
        tree = self.tree
        pos = nx.kamada_kawai_layout(tree, scale=1) # Orientanción

        # Dibujar el árbol
        plt.figure(figsize=(4, 8))  # Tamaño de la figura
        nx.draw(tree, pos, with_labels=True, node_size=400, node_color='lightblue', font_size=8, arrows=False)
        plt.margins(0.2, 0.1)  # Centrar el árbol en la figura
        plt.axis('off')  # Ocultar ejes

        plt.show()