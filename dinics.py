from collections import deque

class Dinic:
    def __init__(self, graph):
        self.graph = graph
        self.residual = {u: {v: graph[u][v] for v in graph[u]} for u in graph}
        self.level = {}

    def bfs(self, source, sink):
        """Builds a level graph using BFS."""
        self.level = {node: -1 for node in self.residual}
        self.level[source] = 0
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v in self.residual[u]:
                if self.level[v] == -1 and self.residual[u][v] > 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)

        return self.level[sink] != -1

    def dfs(self, u, sink, flow):
        """DFS finds augmenting paths with available flow."""
        if u == sink:
            return flow
        for v in self.residual[u]:
            if self.level[v] == self.level[u] + 1 and self.residual[u][v] > 0:
                min_flow = min(flow, self.residual[u][v])
                pushed = self.dfs(v, sink, min_flow)
                if pushed > 0:
                    self.residual[u][v] -= pushed
                    self.residual[v][u] += pushed
                    return pushed
        return 0

    def max_flow(self, source, sink):
        max_flow = 0
        while self.bfs(source, sink):  # for level graph
            while (flow := self.dfs(source, sink, float('Inf'))): 
                max_flow += flow
        return max_flow


dinic = Dinic(graph)
print("Max Flow (Dinic's Algorithm):", dinic.max_flow('S', 'T'))
