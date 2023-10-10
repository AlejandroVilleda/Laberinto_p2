from queue import LifoQueue

# Creación de la estructura de datos del arbol
class Nodo:

    # Inicializando el objeto de la clase
    def __init__(self, Posicion_x = None, Posicion_y = None, Direccion = None, Arriba = None, Abajo = None, Izquierda = None, Derecha = None):
        self.Posicion_x = Posicion_x
        self.Posicion_y = Posicion_y
        self.Direccion = Direccion
        self.Arriba = Arriba
        self.Abajo = Abajo
        self.Derecha = Derecha
        self.Izquierda = Izquierda

    @property
    def Posicion_actual(self): return [self.Posicion_y, self.Posicion_x]

    @property
    def direccion(self): return self.Direccion

class Arbol:

    Nodos_recorridos: list = []       # Nodos que ya hemos recorrido en el arbol
    Nodos_disponibles: Nodo = []      # Colección de nodos por agregar
    Nodos_por_analizar = LifoQueue()     # Colección de nodos dentro del arbol a los que estamos por analizar. LIFO

    # Inicializando
    def __init__(self):
        self.Raiz = None

    # Agregamos un nodo al arbol
    def Agregar(self, Valor): # Recibimos una lista con la posición y la dirección

        #Para el nodo inicial
        if self.Vacio(): self.Raiz = Nodo(Posicion_x = Valor[1], Posicion_y = Valor[0])

        # Para el resto de ramificaciones
        else:
            if(Valor[2] == 'Arriba'):
                aux = self.Raiz
                temp = aux
                Padre_t = None

                #nodo.Arriba = Nodo(Padre = False, Posicion_x = Valor[0], Posicion_y = Valor[1])

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in range(len(Arbol.Instrucciones)):
                    Padre_t = aux.Posicion_actual
                    if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                    if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                    if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                    if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda
                    #aux.Padre = Padre_t
                    Padre_t = aux.Posicion_actual

                if len(Arbol.Instrucciones) == 0: Padre_t = aux.Posicion_actual

                # nodo = temp
                aux.Arriba = Nodo(Padre=Padre_t, Posicion_x=Valor[1], Posicion_y=Valor[0])
                Arbol.Instrucciones.append('Arriba')

            elif(Valor[2] == 'Abajo'):
                aux = self.Raiz
                temp = aux
                Padre_t = None
                # nodo.Arriba = Nodo(Padre = False, Posicion_x = Valor[0], Posicion_y = Valor[1])

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in range(len(Arbol.Instrucciones)):
                    Padre_t = aux.Posicion_actual
                    if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                    if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                    if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                    if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda
                    # aux.Padre = Padre_t
                    Padre_t = aux.Posicion_actual

                if len(Arbol.Instrucciones) == 0: Padre_t = aux.Posicion_actual

                # nodo = temp
                aux.Abajo = Nodo(Padre=Padre_t, Posicion_x=Valor[1], Posicion_y=Valor[0])
                Arbol.Instrucciones.append('Abajo')

            elif (Valor[2] == 'Derecha'):
                aux = self.Raiz
                temp = aux
                Padre_t = None

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in range(len(Arbol.Instrucciones)):
                    Padre_t = aux.Posicion_actual
                    if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                    if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                    if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                    if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda
                    # aux.Padre = Padre_t
                    Padre_t = aux.Posicion_actual

                if len(Arbol.Instrucciones) == 0: Padre_t = aux.Posicion_actual

                Nodo_Auxiliar = Nodo(Padre = Padre_t, Posicion_x=Valor[1], Posicion_y=Valor[0])
                aux.Derecha = Nodo_Auxiliar
                Arbol.Instrucciones.append('Derecha')

            elif (Valor[2] == 'Izquierda'):
                aux = self.Raiz
                temp = aux
                Padre_t = None

                # nodo.Arriba = Nodo(Padre = False, Posicion_x = Valor[0], Posicion_y = Valor[1])

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in range(len(Arbol.Instrucciones)):
                    Padre_t = aux.Posicion_actual
                    if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                    if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                    if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                    if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda
                    # aux.Padre = Padre_t
                    Padre_t = aux.Posicion_actual

                if len(Arbol.Instrucciones) == 0: Padre_t = aux.Posicion_actual

                # nodo = temp
                aux.Izquierda = Nodo(Padre=Padre_t, Posicion_x=Valor[1], Posicion_y=Valor[0])
                Arbol.Instrucciones.append('Izquierda')

    # Agregamos un nodo al arbol
    def Agregar_nodos(self):
        #Nodos disponibles

        if (Arbol.Nodos_disponibles.direccion == 'Arriba'):
            aux = self.Raiz
            temp = aux

            # nodo.Arriba = Nodo(Padre = False, Posicion_x = Valor[0], Posicion_y = Valor[1])

            # Llegamos a la hoja siguiendo las respectivas desiciones generadas
            for i in range(len(Arbol.Instrucciones)):
                if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda


            if len(Arbol.Instrucciones) == 0: Padre_t = aux.Posicion_actual

            aux.Arriba = Nodo(Padre=Padre_t, Posicion_x=Valor[1], Posicion_y=Valor[0])
            Arbol.Instrucciones.append('Arriba')

        pass

    # Agregamos un nodo a la lista de nodos por analizar
    @classmethod
    def Agregar_nodo_LIFO(cls, Nodo):
        cls.Nodos_por_analizar.put(Nodo)

    # Guardamos en una lista los nodos por agregar al arbol
    @classmethod
    def Agregar_nodo(cls, nodo):
        cls.Nodos_disponibles.append(nodo)

    # Mostramos el número de nodos disponibles por analizar
    @classmethod
    def Numero_nodos_analizar(cls): return cls.Nodos_por_analizar.qsize();

    # Obtenemos y retiramos el nodo a analizar con respecto al orden LIFO
    @classmethod
    def Nodo_analizar(cls):
        nodo = cls.Nodos_por_analizar.get()
        cls.Nodos_recorridos.append(nodo)  # Guardamos el nodo como recorrido
        return nodo

    @classmethod
    def Lista_nodos_recorridos(cls):
        return cls.Nodos_recorridos


    def Vacio(self): return self.Raiz == None