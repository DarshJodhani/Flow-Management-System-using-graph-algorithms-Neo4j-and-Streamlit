class PushRelabel:
    def __init__(self, graph):
        self.graph = graph
        self.residual = {u: {v: graph[u][v] for v in graph[u]} for u in graph}
        self.height = {node: 0 for node in self.residual}
        self.excess = {node: 0 for node in self.residual}

    def push(self, u, v):
        """Push flow from u to v if possible."""
        flow = min(self.excess[u], self.residual[u][v])
        self.residual[u][v] -= flow
        self.residual[v][u] += flow
        self.excess[u] -= flow
        self.excess[v] += flow

    def relabel(self, u):
        """Increase the height of node u."""
        min_height = float('Inf')
        for v in self.residual[u]:
            if self.residual[u][v] > 0:
                min_height = min(min_height, self.height[v])
        self.height[u] = min_height + 1

    def max_flow(self, source, sink):
        self.height[source] = len(self.graph)
        for v in self.residual[source]:
            self.push(source, v)

        while True:
            overflow_nodes = [u for u in self.excess if u not in {source, sink} and self.excess[u] > 0]
            if not overflow_nodes:
                break
            for u in overflow_nodes:
                for v in self.residual[u]:
                    if self.residual[u][v] > 0 and self.height[u] == self.height[v] + 1:
                        self.push(u, v)
                self.relabel(u)

        return self.excess[sink]

pr = PushRelabel(graph)
print("Max Flow (Push-Relabel):", pr.max_flow('S', 'T'))
