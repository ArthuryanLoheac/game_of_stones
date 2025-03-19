import sys

def build_friendship_graph(graph, fr, read_file, get_list_pair_friend, find_or_create):
    """
    Construit le graphe d'amitiés à partir du fichier 'fr'.
    """
    friends_list = read_file(fr)
    if not friends_list:
        raise ValueError("Empty friendship file")
    pairs = get_list_pair_friend(friends_list)
    for pair in pairs:
        n1 = find_or_create(graph, pair[0])
        n2 = find_or_create(graph, pair[1])
        n1.add_friend(n2)

def integrate_conspiracies(graph, cr, read_file, get_list_pair_conspiracy):
    """
    Intègre les complots dans le graphe à partir du fichier 'cr'.
    """
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
