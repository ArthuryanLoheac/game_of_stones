import sys
from .chain import compute_candidate_chains, select_disjoint_chains
from .graph_integration import build_friendship_graph, integrate_conspiracies
from .display import print_names, print_relationships

def get_direct_enemies(graph, queenName):
    """
    Retourne la reine (Node) et la liste des ennemis directs (ceux qui complotent contre elle),
    triés par ordre alphabétique.
    """
    queenNode = graph.find_node(queenName)
    if queenNode is None:
        return None, []
    direct_enemies = [node for node in graph.nodes if queenNode in node.conspiration]
    direct_enemies = sorted(set(direct_enemies), key=lambda node: node.name)
    return queenNode, direct_enemies

def execute_links(graph, fr, p1, p2, read_file, get_list_pair_friend, find_or_create, bfs_distance):
    """
    Exécute le mode --links : construit le graphe d'amitiés et affiche le degré de séparation.
    """
    build_friendship_graph(graph, fr, read_file, get_list_pair_friend, find_or_create)
    node1 = graph.find_node(p1)
    node2 = graph.find_node(p2)
    if node1 is None or node2 is None:
        print(f"Degree of separation between {p1} and {p2}: -1")
        return
    distance = bfs_distance(graph, node1, node2)
    print(f"Degree of separation between {p1} and {p2}: {distance}")

def execute_plots(graph, fr, cr, n, read_file, get_list_pair_friend, get_list_pair_conspiracy, find_or_create, bfs_all_distances):
    """
    Exécute le mode --plots : construit le graphe d'amitiés, intègre les complots,
    affiche les noms, la matrice des distances et les chaînes de complot.
    """
    # Construction du graphe et intégration des complots
    build_friendship_graph(graph, fr, read_file, get_list_pair_friend, find_or_create)
    integrate_conspiracies(graph, cr, read_file, get_list_pair_conspiracy)

    # Affichage de la liste des noms et de la matrice des relations
    sorted_names = print_names(graph)
    print_relationships(graph, sorted_names, n, bfs_all_distances)

    # Calcul et sélection des chaînes de complot
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
