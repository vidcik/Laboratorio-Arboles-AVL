import pandas as pd
from graphviz import Digraph


dataset_path = 'dataset_movies (1).csv'
df = pd.read_csv(dataset_path)

print(df.columns)  

class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, node, key, data):
        if not node:
            return AVLNode(key, data)
        if key < node.key:
            node.left = self.insert(node.left, key, data)
        elif key > node.key:
            node.right = self.insert(node.right, key, data)
        else:
            return node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def insert_node(self, key, data):
        self.root = self.insert(self.root, key, data)

    def search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)

    def search_node(self, key):
        return self.search(self.root, key)

    def level_order_traversal(self, node):
        if not node:
            return []
        result = []
        queue = [node]
        while queue:
            current = queue.pop(0)
            result.append(current.key)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return result

    def delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.data = temp.data
            node.right = self.delete(node.right, temp.key)
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def delete_node(self, key):
        self.root = self.delete(self.root, key)

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def find_level(self, root, key, level=1):
        if root is None:
            return 0
        if root.key == key:
            return level
        downlevel = self.find_level(root.left, key, level + 1)
        if downlevel != 0:
            return downlevel
        return self.find_level(root.right, key, level + 1)

    def find_parent(self, node, key, parent=None):
        if node is None:
            return None
        if node.key == key:
            return parent
        if key < node.key:
            return self.find_parent(node.left, key, node)
        else:
            return self.find_parent(node.right, key, node)

    def find_grandparent(self, key):
        parent = self.find_parent(self.root, key)
        if parent:
            return self.find_parent(self.root, parent.key)
        return None

    def find_uncle(self, key):
        parent = self.find_parent(self.root, key)
        grandparent = self.find_grandparent(key)
        if grandparent is None:
            return None
        if grandparent.left == parent:
            return grandparent.right
        else:
            return grandparent.left

    def search_by_criteria(self, node, year, foreign_earnings_min):
        if not node:
            return []
        result = []
        if (node.data['Year'] == year and
            node.data['Domestic Percent'] < node.data['Foreign Percent'] and
            node.data['Foreign Earnings'] >= foreign_earnings_min):
            result.append(node.key)
        result += self.search_by_criteria(node.left, year, foreign_earnings_min)
        result += self.search_by_criteria(node.right, year, foreign_earnings_min)
        return result

def sanitize_node_name(name):
    return name.replace(" ", "_").replace(",", "_").replace(":", "_").replace("'", "_")

def truncate_node_name(name, max_length=30):
    return (name[:max_length] + '...') if len(name) > max_length else name

def visualize_tree(node, graph=None, depth_limit=3, current_depth=0):
    if graph is None:
        graph = Digraph(format='png')
    if node is None:
        return graph
    if current_depth > depth_limit:
        return graph
    sanitized_key = sanitize_node_name(node.key)
    truncated_key = truncate_node_name(sanitized_key)
    graph.node(truncated_key, label=f"{truncated_key}\n{node.data}")
    if node.left:
        sanitized_left_key = sanitize_node_name(node.left.key)
        truncated_left_key = truncate_node_name(sanitized_left_key)
        graph.edge(truncated_key, truncated_left_key)
        visualize_tree(node.left, graph, depth_limit, current_depth + 1)
    if node.right:
        sanitized_right_key = sanitize_node_name(node.right.key)
        truncated_right_key = truncate_node_name(sanitized_right_key)
        graph.edge(truncated_key, truncated_right_key)
        visualize_tree(node.right, graph, depth_limit, current_depth + 1)
    return graph

def render_tree(tree, filename, depth_limit=5):
    dot = visualize_tree(tree.root, depth_limit=depth_limit)
    dot.render(filename, format='png', cleanup=False)
    print(f"Árbol visualizado en {filename}.png")

avl_tree = AVLTree()

# Insertar nodos en el árbol AVL
for index, row in df.iterrows():
    title = row['Title']
    data = row.to_dict()
    avl_tree.insert_node(title, data)

render_tree(avl_tree, 'avl_tree_initial')

#  seleccionar un nodo del dataset para buscarlo e introducirlo del árbol AVL
search_key = "Minions"
found_node = avl_tree.search_node(search_key)
if found_node:
    print(f"Película encontrada: {found_node.key}")

# seleccionar un nodo del dataset para eliminarlo del árbol AVL
delete_key = "Furious 7"
avl_tree.delete_node(delete_key)

render_tree(avl_tree, 'avl_tree_after_deletion')

def get_node_level(tree, key):
    level = tree.find_level(tree.root, key)
    if level:
        print(f"El nivel del nodo '{key}' es: {level}")
    else:
        print(f"El nodo '{key}' no se encontró en el árbol.")

def get_balance_factor(tree, key):
    node = tree.search_node(key)
    if node:
        balance_factor = tree.get_balance(node)
        print(f"El factor de balance del nodo '{key}' es: {balance_factor}")
    else:
        print(f"El nodo '{key}' no se encontró en el árbol.")

def get_parent(tree, key):
    parent = tree.find_parent(tree.root, key)
    if parent:
        print(f"El padre del nodo '{key}' es: {parent.key}")
    else:
        print(f"El nodo '{key}' no tiene padre o no se encontró en el árbol.")

def get_grandparent(tree, key):
    grandparent = tree.find_grandparent(key)
    if grandparent:
        print(f"El abuelo del nodo '{key}' es: {grandparent.key}")
    else:
        print(f"El nodo '{key}' no tiene abuelo o no se encontró en el árbol.")

def get_uncle(tree, key):
    uncle = tree.find_uncle(key)
    if uncle:
        print(f"El tío del nodo '{key}' es: {uncle.key}")
    else:
        print(f"El nodo '{key}' no tiene tío o no se encontró en el árbol.")

#añadir el nodo que se quiere balancear y elegir los datos de abajo
selected_node_key = "Minions"
get_node_level(avl_tree, selected_node_key)
get_balance_factor(avl_tree, selected_node_key)
get_parent(avl_tree, selected_node_key)
get_grandparent(avl_tree, selected_node_key)
get_uncle(avl_tree, selected_node_key)
