from queue import PriorityQueue

# Best First Search Algorithm
def best_first_search(graph, start, goal, heuristic):
    visited = set()  # to keep track of visited nodes
    pq = PriorityQueue()
    pq.put((heuristic[start], start))  # (priority, node)

    print("Best First Search Path:")

    while not pq.empty():
        (h, current_node) = pq.get()
        print(current_node, end=" ")

        if current_node == goal:
            print("\nGoal reached!")
            return

        visited.add(current_node)

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                pq.put((heuristic[neighbor], neighbor))

    print("\nGoal not reachable.")

# Example graph (undirected)
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

# Example heuristic values (lower = closer to goal)
heuristic = {
    'A': 10,
    'B': 8,
    'C': 5,
    'D': 7,
    'E': 3,
    'F': 6,
    'G': 0  # Goal node
}

# Run Best First Search
best_first_search(graph, 'A', 'G', heuristic)
