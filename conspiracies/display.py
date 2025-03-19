def print_names(graph):
    """
    Affiche la liste alphabétique des noms présents dans le graphe
    et retourne cette liste.
    """
    sorted_names = sorted(node.name for node in graph.nodes)
    print("Names:")
    for name in sorted_names:
        print(name)
    print()
    return sorted_names

def print_relationships(graph, sorted_names, n, bfs_all_distances):
    """
    Affiche la matrice des distances entre les personnages.
    Si la distance > n, affiche 0 ; si inaccessible, affiche -1.
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
