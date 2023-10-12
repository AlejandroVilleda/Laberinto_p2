import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import time

# Crear un grafo dirigido (DiGraph) para representar el árbol
tree = nx.DiGraph()

# Agregar nodos y aristas a tu árbol (ajusta según tu estructura de árbol)
tree.add_node((9,0))
tree.add_node((9,1))
tree.add_node((2,1))
tree.add_edge((9,0), (9,1))
tree.add_edge((9,1), (8,1))

# Obtener la disposición (layout) con "kamada_kawai_layout" para respetar la jerarquía de profundidad
pos = nx.kamada_kawai_layout(tree, scale=1)

# Dibujar el árbol
plt.figure(figsize=(4, 8))  # Tamaño de la figura
nx.draw(tree, pos, with_labels=True, node_size=400, node_color='lightblue', font_size=8, arrows = False)
# Centrar el árbol en la figura
plt.margins(0.2, 0.1)
plt.axis('off')  # Ocultar ejes

for i in range(5):
    plt.figure(figsize=(4, 8))  # Tamaño de la figura
    nx.draw(tree, pos, with_labels=True, node_size=400, node_color='lightblue', font_size=8, arrows=False)
    plt.show()
    time.sleep(2)
    print("Paou")
    tree.add_node((6, i))
    tree.add_node((i, 3))

