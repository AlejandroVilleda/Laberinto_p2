"""
Creación de la estructura de datos del arbol"""
class Nodo:

    # Inicializando el objeto de la clase
    def __init__(self, Padre = False, Arriba = None, Abajo = None, Izquierda = None, Derecha = None, Posicion_x = None, Posicion_y = None):
        self.Padre = Padre
        self.Arriba = Arriba
        self.Abajo = Abajo
        self.Derecha = Derecha
        self.Izquierda = Izquierda
        self.Posicion_x = Posicion_x
        self.Posicion_y = Posicion_y

    @property
    def Valor_padre(self):
        return [self.Posicion_y, self.Posicion_x]


class Arbol:

    Instrucciones = []

    # Inicializando
    def __init__(self):
        self.Raiz = None

    # Agregamos un nodo al arbol
    def Agregar(self, Valor): # Recibimos una lista con la posición y la dirección
        #Para el nodo inicial
        if self.Vacio():
            self.Raiz = Nodo(Padre = True, Posicion_x = Valor[1], Posicion_y = Valor[0])

        # Para el resto de ramificaciones
        else:
            if(Valor[2] == 'Arriba'):
                aux = self.Raiz
                temp = aux
                Padre_t = None

                #nodo.Arriba = Nodo(Padre = False, Posicion_x = Valor[0], Posicion_y = Valor[1])

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in range(len(Arbol.Instrucciones)):
                    Padre_t = aux.Valor_padre
                    if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                    if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                    if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                    if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda
                    #aux.Padre = Padre_t
                    Padre_t = aux.Valor_padre

                if len(Arbol.Instrucciones) == 0: Padre_t = aux.Valor_padre

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
                    Padre_t = aux.Valor_padre
                    if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                    if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                    if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                    if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda
                    # aux.Padre = Padre_t
                    Padre_t = aux.Valor_padre

                if len(Arbol.Instrucciones) == 0: Padre_t = aux.Valor_padre

                # nodo = temp
                aux.Abajo = Nodo(Padre=Padre_t, Posicion_x=Valor[1], Posicion_y=Valor[0])
                Arbol.Instrucciones.append('Abajo')

            elif (Valor[2] == 'Derecha'):
                aux = self.Raiz
                temp = aux
                Padre_t = None

                # Llegamos a la hoja siguiendo las respectivas desiciones generadas
                for i in range(len(Arbol.Instrucciones)):
                    Padre_t = aux.Valor_padre
                    if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                    if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                    if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                    if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda
                    # aux.Padre = Padre_t
                    Padre_t = aux.Valor_padre

                if len(Arbol.Instrucciones) == 0: Padre_t = aux.Valor_padre

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
                    Padre_t = aux.Valor_padre
                    if Arbol.Instrucciones[i] == 'Arriba': aux = aux.Arriba
                    if Arbol.Instrucciones[i] == 'Abajo': aux = aux.Abajo
                    if Arbol.Instrucciones[i] == 'Derecha': aux = aux.Derecha
                    if Arbol.Instrucciones[i] == 'Izquierda': aux = aux.Izquierda
                    # aux.Padre = Padre_t
                    Padre_t = aux.Valor_padre

                if len(Arbol.Instrucciones) == 0: Padre_t = aux.Valor_padre

                # nodo = temp
                aux.Izquierda = Nodo(Padre=Padre_t, Posicion_x=Valor[1], Posicion_y=Valor[0])
                Arbol.Instrucciones.append('Izquierda')

    def Contar_Hijos(self):
        aux = 0
        nodo = self.Raiz

        if (nodo.Arriba != None): aux += 1
        if (nodo.Abajo != None): aux += 1
        if (nodo.Derecha != None): aux += 1
        if (nodo.Izquierda != None): aux += 1

        return aux

    def Padre(self):

        pass

    def Avanzar(self):
        aux = self.Raiz
        temp = None

        while(aux.Arriba != None):
        #if (nodo.Arriba != None):
            temp = aux
            aux = aux.Arriba

        while (aux.Abajo != None):
            temp = aux
            aux = aux.Abajo

        while (aux.Derecha != None):
            temp = aux
            aux = aux.Derecha

        while (aux.Izquierda != None):
            temp = aux
            aux = aux.Izquierda


        #if (nodo.Izquierda != None): nodo = nodo.Izquierda
        nodo = temp

    def Avance_particular(self, Direccion):
        nodo = self.Raiz

        #Tomamos la dirección que recibamos en el parametro
        if Direccion == 'Arriba':nodo = nodo.Arriba
        if Direccion == 'Abajo': nodo = nodo.Abajo
        if Direccion == 'Derecha': nodo = nodo.Derecha
        if Direccion == 'Izquierda':nodo = nodo.Izquierda

    @property
    def Valor_Padre(self):
        Nodo = self.Raiz

        for i in range(len(Arbol.Instrucciones)):
            if Arbol.Instrucciones[i] == 'Arriba': Nodo = Nodo.Arriba
            if Arbol.Instrucciones[i] == 'Abajo': Nodo = Nodo.Abajo
            if Arbol.Instrucciones[i] == 'Derecha': Nodo = Nodo.Derecha
            if Arbol.Instrucciones[i] == 'Izquierda': Nodo = Nodo.Izquierda

        print(Arbol.Instrucciones)
        print(Nodo.Valor_padre)
        return Nodo.Padre


    def Vacio(self):
        return self.Raiz == None


"""        Nodo = self.Raiz

        for i in range(len(Arbol.Instrucciones) - 1):
            if Arbol.Instrucciones[i] == 'Arriba': Nodo = Nodo.Arriba
            if Arbol.Instrucciones[i] == 'Abajo': Nodo = Nodo.Abajo
            if Arbol.Instrucciones[i] == 'Derecha': Nodo = Nodo.Derecha
            if Arbol.Instrucciones[i] == 'Izquierda': Nodo = Nodo.Izquierda

        return Nodo.Valor_padre"""


