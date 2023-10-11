import queue

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
    Nodos_por_incluir = queue.Queue()  # Cola de prioridad para insertar nodos al arbol
    Nodos_recorridos: list = []      # Lista de nodos ya recorridos en el arbol
    Direccion_nodos: list = []       # Lista de direcciones para llegar a la hoja

    # Inicio del arbol vacio
    def __init__(self): self.Inicio = None

    def Generar_nodos(self, Direccion):

        # Si esta vacio el arbol
        if self.Vacio() == True:
            Nuevo_Nodo: Nodo = Arbol.Nodos_por_incluir.get()  # Obtenemos el único nodo que debe existir en el queue
            self.Inicio = Nuevo_Nodo    # Lo ingresamos como inicio del arbol

            Arbol.Nodos_recorridos.append(Nuevo_Nodo.Posicion_actual)  # Colocamos la posición del nodo como recorrido

        # si no esta vacio
        else:
            # Evaluamos las direcciones en las que debemos desarrollar el arbol
            if Direccion == "Arriba":
                aux = self.Inicio

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in Arbol.Direccion_nodos:
                    if i == 'Arriba': aux = aux.Arriba
                    if i == 'Abajo': aux = aux.Abajo
                    if i == 'Derecha': aux = aux.Derecha
                    if i == 'Izquierda': aux = aux.Izquierda

                Nuevo_nodo: Nodo = Arbol.Nodos_por_incluir.get()
                aux.Arriba = Nuevo_nodo
                Arbol.Nodos_recorridos.append(Nuevo_nodo.Posicion_actual)

            if Direccion == "Abajo":
                aux = self.Inicio

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in Arbol.Direccion_nodos:
                    if i == 'Arriba': aux = aux.Arriba
                    if i == 'Abajo': aux = aux.Abajo
                    if i == 'Derecha': aux = aux.Derecha
                    if i == 'Izquierda': aux = aux.Izquierda

                Nuevo_nodo: Nodo = Arbol.Nodos_por_incluir.get()
                aux.Abajo = Nuevo_nodo
                Arbol.Nodos_recorridos.append(Nuevo_nodo.Posicion_actual)

            if Direccion == "Derecha":
                aux = self.Inicio

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in Arbol.Direccion_nodos:
                    if i == 'Arriba': aux = aux.Arriba
                    if i == 'Abajo': aux = aux.Abajo
                    if i == 'Derecha': aux = aux.Derecha
                    if i == 'Izquierda': aux = aux.Izquierda

                Nuevo_nodo: Nodo = Arbol.Nodos_por_incluir.get()
                aux.Derecha = Nuevo_nodo
                Arbol.Nodos_recorridos.append(Nuevo_nodo.Posicion_actual)

            if Direccion == "Izquierda":
                aux = self.Inicio

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in Arbol.Direccion_nodos:
                    if i == 'Arriba': aux = aux.Arriba
                    if i == 'Abajo': aux = aux.Abajo
                    if i == 'Derecha': aux = aux.Derecha
                    if i == 'Izquierda': aux = aux.Izquierda

                Nuevo_nodo: Nodo = Arbol.Nodos_por_incluir.get()
                aux.Izquierda = Nuevo_nodo
                Arbol.Nodos_recorridos.append(Nuevo_nodo.Posicion_actual)

            pass



    # Agregamos los nodos a una queue para posteriormente ingresarlos en el arbol
    def Agregar_nodo_FIFO(self, nodo): self.Nodos_por_incluir.put(nodo)

    # Agregamos la dirección o ruta que debe seguir el arbol para ingresar el nodo
    def Agregar_direccion_nodo(self, direccion): self.Direccion_nodos.append(direccion)

    # Verifica que el arbol esté vacio
    def Vacio(self): return self.Inicio == None