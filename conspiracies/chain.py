from collections import deque

def find_conspiracy_chain_for_enemy(graph, enemy, n, dist_from_queen, queenNode):
    """
    Cherche une chaîne de complot depuis un ami proche de la reine (distance <= n)
    jusqu'à l'ennemi direct, sans répétition de personnage dans la chaîne.
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

def compute_candidate_chains(graph, direct_enemies, n, dist_from_queen, queenNode):
    """
    Pour chaque ennemi direct, calcule la chaîne candidate (si possible).
    Retourne un dictionnaire {enemy.name: chain}.
    """
    candidate_chains = {}
    for enemy in direct_enemies:
        chain = find_conspiracy_chain_for_enemy(graph, enemy, n, dist_from_queen, queenNode)
        if chain is not None:
            candidate_chains[enemy.name] = chain
    return candidate_chains

def select_disjoint_chains(direct_enemies, candidate_chains):
    """
    Sélectionne pour chaque ennemi une chaîne disjointe (sans chevauchement des maillons, sauf la cible).
    Retourne (selected, no_chain) où 'selected' est un dictionnaire {enemy.name: chain}
    et 'no_chain' un ensemble des ennemis pour lesquels aucune chaîne n'a pu être assignée.
    """
    selected = {}
    used_nodes = set()
    no_chain = set()
    for enemy in direct_enemies:
        if enemy.name in candidate_chains:
            chain = candidate_chains[enemy.name]
            chain_nodes = set(chain[:-1])  # Exclure la cible
            if used_nodes & chain_nodes:
                no_chain.add(enemy.name)
            else:
                selected[enemy.name] = chain
                used_nodes |= chain_nodes
        else:
            no_chain.add(enemy.name)
    return selected, no_chain
