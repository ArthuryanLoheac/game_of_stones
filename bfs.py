from collections import deque

def bfs_distance(graph, start, end):
    """Retourne la distance (nombre de liens) entre 'start' et 'end'."""
    for node in graph.nodes:
        node.depth = -1
    queue = deque()
    start.depth = 0
    queue.append(start)
    while queue:
        current = queue.popleft()
        if current == end:
            return current.depth
        for friend in current.friends:
            if friend.depth == -1:
                friend.depth = current.depth + 1
                queue.append(friend)
    return -1

def bfs_all_distances(graph, start):
    """
    Retourne un dictionnaire {node: distance} pour tous les nœuds accessibles
    depuis 'start' dans le graphe.
    """
    for node in graph.nodes:
        node.depth = -1
    dist = {}
    queue = deque()
    start.depth = 0
    dist[start] = 0
    queue.append(start)
    while queue:
        current = queue.popleft()
        for friend in current.friends:
            if friend.depth == -1:
                friend.depth = current.depth + 1
                dist[friend] = friend.depth
                queue.append(friend)
    return dist
