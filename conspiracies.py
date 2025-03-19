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
        queue = deque()
        queue.append((node, [node]))
        while queue:
            current, path = queue.popleft()
            for neighbor in current.conspiration:
                if neighbor in path:
                    continue
                new_path = path + [neighbor]
                if neighbor == enemy:
                    candidate_chains.append(new_path)
                else:
                    queue.append((neighbor, new_path))
    if not candidate_chains:
        return None

    def chain_priority(chain):
        S = chain[0]
        is_direct = 1 if queenNode in S.conspiration else 0
        return (len(chain), is_direct, dist_from_queen.get(S, 9999), S.name, [node.name for node in chain])
    candidate_chains.sort(key=chain_priority)
    best_chain = candidate_chains[0]
    return [node.name for node in best_chain]

def execute_links(graph, fr, p1, p2, read_file, get_list_pair_friend, find_or_create, bfs_distance):
    """Exécute le mode --links."""
    friends_list = read_file(fr)
    if not friends_list:
        raise ValueError("Empty friendship file")
    pairs = get_list_pair_friend(friends_list)
    for pair in pairs:
        n1 = find_or_create(graph, pair[0])
        n2 = find_or_create(graph, pair[1])
        n1.add_friend(n2)
    node1 = graph.find_node(p1)
    node2 = graph.find_node(p2)
    if node1 is None or node2 is None:
        print(f"Degree of separation between {p1} and {p2}: -1")
        return
    distance = bfs_distance(graph, node1, node2)
    print(f"Degree of separation between {p1} and {p2}: {distance}")

def execute_plots(graph, fr, cr, n, read_file, get_list_pair_friend, get_list_pair_conspiracy, find_or_create, bfs_all_distances):
    """Exécute le mode --plots."""
    # Construction du graphe d'amitiés
    friends_list = read_file(fr)
    if not friends_list:
        raise ValueError("Empty friendship file")
    pairs = get_list_pair_friend(friends_list)
    for pair in pairs:
        n1 = find_or_create(graph, pair[0])
        n2 = find_or_create(graph, pair[1])
        n1.add_friend(n2)

    # Intégration des complots
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

    # Affichage de la liste alphabétique
    sorted_names = sorted(node.name for node in graph.nodes)
    print("Names:")
    for name in sorted_names:
        print(name)
    print()

    # Matrice des distances
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

    # Recherche de chaînes de complot
    queenName = "Cersei Lannister"
    queenNode = graph.find_node(queenName)
    if queenNode is None:
        print("Conspiracies:")
        print("No queen in the graph => no resolution possible.")
        print()
        print("Result:")
        print("There is only one way out: treason!")
        return

    dist_from_queen = bfs_all_distances(graph, queenNode)
    direct_enemies = []
    for node in graph.nodes:
        if queenNode in node.conspiration:
            direct_enemies.append(node)
    direct_enemies = sorted(set(direct_enemies), key=lambda node: node.name)

    candidate_chains = {}
    for enemy in direct_enemies:
        chain = find_conspiracy_chain_for_enemy(graph, enemy, n, dist_from_queen, queenNode)
        if chain is not None:
            candidate_chains[enemy.name] = chain

    selected = {}
    used_nodes = set()
    no_chain = set()
    for enemy in direct_enemies:
        if enemy.name in candidate_chains:
            chain = candidate_chains[enemy.name]
            chain_nodes = set(chain[:-1])
            if used_nodes & chain_nodes:
                no_chain.add(enemy.name)
            else:
                selected[enemy.name] = chain
                used_nodes |= chain_nodes
        else:
            no_chain.add(enemy.name)

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
