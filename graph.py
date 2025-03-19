class Node:
    """Représente un personnage avec ses amis et ses complots."""
    def __init__(self, name: str):
        self.name = name
        self.friends = []
        self.conspiration = []  # Liste des nœuds contre lesquels ce personnage complote
        self.depth = -1

    def __hash__(self):
        return hash(self.name)

    def add_friend(self, friend: 'Node'):
        """Ajoute une relation d'amitié bi-directionnelle."""
        if friend.name == self.name:
            raise ValueError("Cannot be friend with himself")
        if friend not in self.friends:
            self.friends.append(friend)
        if self not in friend.friends:
            friend.friends.append(self)

    def add_conspiration(self, target: 'Node'):
        """Ajoute un complot orienté : ce personnage complote contre target."""
        if target.name == self.name:
            raise ValueError("Cannot conspire against himself")
        if target not in self.conspiration:
            self.conspiration.append(target)

class Graph:
    """Graphe global contenant les nœuds."""
    def __init__(self):
        self.nodes = []

    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes.append(node)
        else:
            raise ValueError("Node already exists")

    def find_node(self, name: str) -> Node:
        for node in self.nodes:
            if node.name == name:
                return node
        return None

def find_or_create(graph: Graph, name: str) -> Node:
    """Retourne le nœud portant le nom 'name', ou le crée s'il n'existe pas."""
    node = graph.find_node(name)
    if node is None:
        node = Node(name)
        graph.add_node(node)
    return node
