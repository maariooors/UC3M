"""
Case #2. Exercise  3
@author: EDA Team
"""

# Classes provided by EDA Team
from dlist import DList
from bintree import BinaryNode
from bst import BinarySearchTree

class BST2(BinarySearchTree):
    def find_dist_k(self, n: int, k:int) -> list:
        
        # Donde n: Es el elemento a buscar, y k: la distancia
        
        # Primero vamos a sacar que nodo contiene a dicho elemento, para posteriormente
        # buscar su altura.
        # Para ello usaremos el método self.search() para encontrar el elemento en el árbol,
        # esto nos devolverá el nodo en el que se encuentra y después se lo pasaremos a 
        # self.depth() para que encuentre su altura.
        
        # Primero evaluaremos los casos base
        
        if not isinstance(n, int) or not isinstance(k, int):
            #print("Los elementos introducidos no son números")
            return
        
        elif not self.root:
            #print("Error: No existe ningún árbol")
            return
            
        elif k < 0:
            return 
        
        elif self.search(n):
            node_target = self.search(n)     # Nodo del elemento
            prof = self.depth(node_target)   # Profundidad del nodo
            lista_nodos = []
            self._find_dist_k(self.root, (k - prof), n, True, lista_nodos)
            return lista_nodos
        else:
            #print("El elemento que has indicado no está en el árbol")
            return  
        
    def _find_dist_k(self, node: BinaryNode, k: int, n: int, direcion: bool, lista_nodos: list) -> None:
                    
        if not node: # Porque una vez que es negativo no va a ser positivo nunca más
            return
            
        if k < 0:
            if node.elem < n:
                self._find_dist_k(node.right, k + 1, n, True, lista_nodos) # Para coger el primer nodo a la dercha
            
            else: # node.elem > n:
                self._find_dist_k(node.left, k + 1, n, True, lista_nodos)
                
        elif k == 0:
            
            lista_nodos.append(node.elem)

            if node.elem > n and direcion:
                self._find_dist_k(node.left, k + 1, n, True, lista_nodos)
            elif node.elem < n and direcion:
                self._find_dist_k(node.right, k + 1, n, True, lista_nodos)
        else:
              
            if node.elem == n:
                direcion = False

            if node.elem > n and direcion:
                self._find_dist_k(node.left, k + 1, n, True, lista_nodos)
                self._find_dist_k(node.right, k - 1, n, False, lista_nodos)
            
            elif node.elem < n and direcion:
                self._find_dist_k(node.left, k - 1, n, False, lista_nodos)
                self._find_dist_k(node.right, k + 1, n, True, lista_nodos)
                
            else:
                self._find_dist_k(node.left, k - 1, n, False, lista_nodos)
                self._find_dist_k(node.right, k - 1, n, False, lista_nodos) 
            


def create_tree(input_tree1: BinarySearchTree, input_tree2: BinarySearchTree, opc: str) -> BinarySearchTree:
    ...
    create_tree()

# Some usage examples
if __name__ == '__main__':
    input_list = [50, 55, 54, 20, 60, 15, 18, 5, 25, 24, 75, 80]
    # input_list_01 = [5, 1, 7, 9, 23]
    # input_list_02 = [1, 9, 11]

    input_list_01 = [5, 12, 2, 1, 3, 9]
    input_list_02 = [9, 3, 21]

    # Build and draw first tree
    tree1 = BinarySearchTree()
    for x in input_list_01:
        tree1.insert(x)
    tree1.draw()

    # Build and draw second tree
    tree2 = BinarySearchTree()
    for x in input_list_02:
        tree2.insert(x)
    tree2.draw()

    function_names = ["merge", "intersection", "difference"]

    for op_name in function_names:
        res = create_tree(tree1, tree2, op_name)
        print(f"-- Result for {op_name} method. #{res.size()} nodes")
        res.draw()
