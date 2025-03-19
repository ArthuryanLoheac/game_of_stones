# conspiracies.py
from collections import deque
import sys

def find_conspiracy_chain_for_enemy(graph, enemy, n, dist_from_queen, queenNode):
    """
    Cherche une chaîne de complot depuis un ami proche de la reine (distance <= n)
    jusqu'à l'ennemi direct, sans répéter de personnage dans la chaîne.
    Retourne la chaîne sous forme d'une liste de noms, ou None.
    """
    candidate_chains = []
    for node in graph.nodes:
        if node == enemy:
            continue
        if node not in dist_from_queen or dist_from_queen[node] > n:
            continue
        # Effectuer une recherche en largeur dans le graphe des complots depuis ce nœud
        queue = deque()
        queue.append((node, [node]))
        while queue:
            current, path = queue.popleft()
            for neighbor in current.conspiration:
                if neighbor in path:  # éviter les cycles
                    continue
                new_path = path + [neighbor]
                if neighbor == enemy:
                    candidate_chains.append(new_path)
                else:
                    queue.append((neighbor, new_path))
    if not candidate_chains:
        return None

    def chain_priority(chain):
        # Pour le point de départ S de la chaîne, is_direct vaut 1 s'il complote directement contre la reine, 0 sinon
        S = chain[0]
        is_direct = 1 if queenNode in S.conspiration else 0
        return (len(chain), is_direct, dist_from_queen.get(S, 9999), S.name, [node.name for node in chain])
    
    candidate_chains.sort(key=chain_priority)
    best_chain = candidate_chains[0]
    return [node.name for node in best_chain]

# --- Fonctions pour la construction du graphe et l'intégration des données ---

def build_friendship_graph(graph, fr, read_file, get_list_pair_friend, find_or_create):
    """Construit le graphe d'amitiés à partir du fichier 'fr'."""
    friends_list = read_file(fr)
    if not friends_list:
        raise ValueError("Empty friendship file")
    pairs = get_list_pair_friend(friends_list)
    for pair in pairs:
        n1 = find_or_create(graph, pair[0])
        n2 = find_or_create(graph, pair[1])
        n1.add_friend(n2)

def integrate_conspiracies(graph, cr, read_file, get_list_pair_conspiracy):
    """Intègre les complots dans le graphe à partir du fichier 'cr'."""
    conspiracies_list = read_file(cr)
    if not conspiracies_list:
        raise ValueError("Empty conspiracies file")
    conspiracy_pairs = get_list_pair_conspiracy(conspiracies_list)
    for pair in conspiracy_pairs:
        A, B = pair
        nodeA = graph.find_node(A)
        nodeB = graph.find_node(B)
        if nodeA is None or nodeB is None:
            print(f"An error occurred: {A if nodeA is None else B} not found in friendships file", file=sys.stderr)
            sys.exit(84)
        nodeA.add_conspiration(nodeB)

# --- Fonctions d'affichage ---

def print_names(graph):
    """Affiche la liste alphabétique des noms présents dans le graphe."""
    sorted_names = sorted(node.name for node in graph.nodes)
    print("Names:")
    for name in sorted_names:
        print(name)
    print()
    return sorted_names

def print_relationships(graph, sorted_names, n, bfs_all_distances):
    """
    Affiche la matrice des distances entre les personnages.
    Si la distance est > n, affiche 0, et -1 si inaccessible.
    """
    print("Relationships:")
    for name1 in sorted_names:
        src_node = graph.find_node(name1)
        dist_dict = bfs_all_distances(graph, src_node)
        row_parts = []
        for name2 in sorted_names:
            dst_node = graph.find_node(name2)
            if dst_node in dist_dict:
                d = dist_dict[dst_node]
                row_parts.append(str(d if d <= n else 0))
            else:
                row_parts.append(str(-1))
        print(" ".join(row_parts))
    print()

# --- Fonctions de calcul et sélection des chaînes de complot ---

def get_direct_enemies(graph, queenName):
    """Retourne la liste des ennemis directs (ceux qui complotent contre la reine)."""
    queenNode = graph.find_node(queenName)
    if queenNode is None:
        return None, []
    direct_enemies = [node for node in graph.nodes if queenNode in node.conspiration]
    direct_enemies = sorted(set(direct_enemies), key=lambda node: node.name)
    return queenNode, direct_enemies

def compute_candidate_chains(graph, direct_enemies, n, dist_from_queen, queenNode):
    """Pour chaque ennemi direct, cherche une chaîne candidate."""
    candidate_chains = {}
    for enemy in direct_enemies:
        chain = find_conspiracy_chain_for_enemy(graph, enemy, n, dist_from_queen, queenNode)
        if chain is not None:
            candidate_chains[enemy.name] = chain
    return candidate_chains

def select_disjoint_chains(direct_enemies, candidate_chains):
    """
    Sélectionne pour chaque ennemi une chaîne disjointe (les maillons de la chaîne ne se chevauchent pas).
    Retourne un dictionnaire mapping enemy.name -> chaîne et un ensemble d'ennemis sans chaîne.
    """
    selected = {}
    used_nodes = set()
    no_chain = set()
    for enemy in direct_enemies:
        if enemy.name in candidate_chains:
            chain = candidate_chains[enemy.name]
            # Exclure la cible (dernier élément) de la vérification de conflits
            chain_nodes = set(chain[:-1])
            if used_nodes & chain_nodes:
                no_chain.add(enemy.name)
            else:
                selected[enemy.name] = chain
                used_nodes |= chain_nodes
        else:
            no_chain.add(enemy.name)
    return selected, no_chain

# --- Fonctions d'exécution des modes ---

def execute_links(graph, fr, p1, p2, read_file, get_list_pair_friend, find_or_create, bfs_distance):
    """Exécute le mode --links."""
    build_friendship_graph(graph, fr, read_file, get_list_pair_friend, find_or_create)
    node1 = graph.find_node(p1)
    node2 = graph.find_node(p2)
    if node1 is None or node2 is None:
        print(f"Degree of separation between {p1} and {p2}: -1")
        return
    distance = bfs_distance(graph, node1, node2)
    print(f"Degree of separation between {p1} and {p2}: {distance}")

def execute_plots(graph, fr, cr, n, read_file, get_list_pair_friend, get_list_pair_conspiracy, find_or_create, bfs_all_distances):
    """Exécute le mode --plots."""
    # 1. Construction du graphe d'amitiés et intégration des complots
    build_friendship_graph(graph, fr, read_file, get_list_pair_friend, find_or_create)
    integrate_conspiracies(graph, cr, read_file, get_list_pair_conspiracy)

    # 2. Affichage de la liste des noms et de la matrice des relations
    sorted_names = print_names(graph)
    print_relationships(graph, sorted_names, n, bfs_all_distances)

    # 3. Recherche et sélection des chaînes de complot
    queenName = "Cersei Lannister"
    queenNode, direct_enemies = get_direct_enemies(graph, queenName)
    if queenNode is None:
        print("Conspiracies:")
        print("No queen in the graph => no resolution possible.")
        print()
        print("Result:")
        print("There is only one way out: treason!")
        return

    dist_from_queen = bfs_all_distances(graph, queenNode)
    candidate_chains = compute_candidate_chains(graph, direct_enemies, n, dist_from_queen, queenNode)
    selected, no_chain = select_disjoint_chains(direct_enemies, candidate_chains)

    # 4. Affichage des chaînes et du résultat
    final_chains = list(selected.values())
    final_chains.sort(key=lambda chain: (len(chain), chain))
    
    print("Conspiracies:")
    for chain in final_chains:
        print(" -> ".join(chain))
    for enemy in sorted(no_chain):
        print(f"No conspiracy possible against {enemy}")
    print()

    if len(selected) != len(direct_enemies):
        print("Result:")
        print("There is only one way out: treason!")
    else:
        print("Result:")
        print("The stone is safe!")
