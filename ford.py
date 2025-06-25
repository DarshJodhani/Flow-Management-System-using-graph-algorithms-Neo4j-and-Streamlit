from collections import deque

class FordFulkerson:
    def __init__(self, graph):
        self.graph = graph  
        self.residual = {u: {v: graph[u][v] for v in graph[u]} for u in graph}  

    def bfs(self, source, sink, parent):
        """Finds an augmenting path using BFS and stores the path in `parent`."""
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v in self.residual[u]:
                if v not in visited and self.residual[u][v] > 0:
                    queue.append(v)
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def max_flow(self, source, sink):
        parent = {}
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float('Inf')
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.residual[u][v])
                v = u
                
            v = sink
            while v != source:
                u = parent[v]
                self.residual[u][v] -= path_flow
                self.residual[v][u] += path_flow 
                v = u

            max_flow += path_flow

        return max_flow