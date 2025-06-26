import uuid
from neo4j import GraphDatabase
# MATCH (n)-[r]->(m)
# RETURN n, r, m

NEO4J_URI = "your uri" 
NEO4J_USER = "user"
NEO4J_PASSWORD = "your password"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
import json
import random
import tempfile
import webbrowser


def init_session():
    if "graph" not in st.session_state:
        st.session_state.graph = nx.DiGraph()
    if "source" not in st.session_state:
        st.session_state.source = 0
    if "sink" not in st.session_state:
        st.session_state.sink = 5

init_session()

def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    edge_labels = {(u, v): f"{G[u][v]['capacity']}" for u, v in G.edges()}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    st.pyplot(plt)

def run_ford_fulkerson():
    G = st.session_state.graph.copy()
    source, sink = st.session_state.source, st.session_state.sink
    start_time = time.time()
    max_flow = nx.maximum_flow(G, source, sink)[0]
    end_time = time.time()
    st.success(f"Max Flow (Ford-Fulkerson): {max_flow}")
    st.info(f"Execution Time: {end_time - start_time:.6f} seconds")

def run_dinic():
    G = st.session_state.graph.copy()
    source, sink = st.session_state.source, st.session_state.sink
    start_time = time.time()
    max_flow = nx.maximum_flow(G, source, sink)[0]
    end_time = time.time()
    st.success(f"Max Flow (Dinic’s Algorithm): {max_flow}")
    st.info(f"Execution Time: {end_time - start_time:.6f} seconds")

def run_push_relabel():
    G = st.session_state.graph.copy()
    source, sink = st.session_state.source, st.session_state.sink
    start_time = time.time()
    max_flow = nx.maximum_flow_value(G, source, sink, flow_func=nx.algorithms.flow.preflow_push)
    end_time = time.time()
    st.success(f"Max Flow (Push-Relabel): {max_flow}")
    st.info(f"Execution Time: {end_time - start_time:.6f} seconds")

def calculate_min_cut():
    G = st.session_state.graph.copy()
    source, sink = st.session_state.source, st.session_state.sink
    cut_value, (reachable, non_reachable) = nx.minimum_cut(G, source, sink)
    min_cut_edges = [(u, v) for u in reachable for v in non_reachable if G.has_edge(u, v)]
    st.success(f"Minimum Cut Value: {cut_value}")
    st.write("Edges in the Minimum Cut:")
    for edge in min_cut_edges:
        st.write(f"{edge[0]} → {edge[1]} (Capacity: {G[edge[0]][edge[1]]['capacity']})")
        
def add_edge(u, v, capacity):
    st.session_state.graph.add_edge(u, v, capacity=capacity)

def remove_edge(u, v):
    if st.session_state.graph.has_edge(u, v):
        st.session_state.graph.remove_edge(u, v)

def generate_random_graph(n, m):
    """Generate a fully connected directed graph with exactly m edges."""
    if m < n - 1:
        st.error("The number of edges must be at least (n-1) for full connectivity!")
        return
    
    G = nx.DiGraph()
    nodes = list(range(n))
    random.shuffle(nodes)  

    for i in range(n - 1):
        u, v = nodes[i], nodes[i + 1]
        capacity = random.randint(5, 20)
        G.add_edge(u, v, capacity=capacity)

    extra_edges = m - (n - 1)
    existing_edges = set(G.edges())

    while extra_edges > 0:
        u, v = random.sample(nodes, 2)  
        if (u, v) not in existing_edges:
            capacity = random.randint(5, 20)
            G.add_edge(u, v, capacity=capacity)
            existing_edges.add((u, v))
            extra_edges -= 1

    st.session_state.graph = G
    st.success(f"Random Graph with {n} nodes and {m} edges generated successfully!")

def save_graph_to_neo4j(graph_id):
    G = st.session_state.graph
    
    if not graph_id:
        st.error("Please enter a valid Graph ID before saving!")
        return

    with driver.session() as session:
        for u, v in G.edges():
            capacity = G[u][v]["capacity"]
            session.run("""
                MERGE (a:Node {id: $u, graph_id: $graph_id})
                MERGE (b:Node {id: $v, graph_id: $graph_id})
                MERGE (a)-[:FLOW {capacity: $capacity, graph_id: $graph_id}]->(b)
            """, u=u, v=v, capacity=capacity, graph_id=graph_id)

    st.success(f"Graph saved successfully with ID: {graph_id}")

def load_graph_from_neo4j(graph_id):
    G = nx.DiGraph()
    
    if not graph_id:
        st.error("Please enter a valid Graph ID before loading!")
        return
    
    with driver.session() as session:
        result = session.run("MATCH (a)-[r:FLOW {graph_id: $graph_id}]->(b) RETURN a.id, b.id, r.capacity", graph_id=graph_id)
        for record in result:
            u, v, capacity = record["a.id"], record["b.id"], record["r.capacity"]
            G.add_edge(u, v, capacity=capacity)
    
    st.session_state.graph = G
    st.success(f"Graph loaded successfully with ID: {graph_id}")

def upload_graph(file):
    G = nx.DiGraph()
    for line in file.getvalue().decode("utf-8").split("\n"):
        if line.strip():
            u, v, cap = map(int, line.split())
            G.add_edge(u, v, capacity=cap)
    st.session_state.graph = G
    st.success("Graph uploaded successfully!")

def open_graph_new_tab():
    G = st.session_state.graph
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        with open(tmpfile.name, "w") as f:
            f.write("<html><body><pre>Graph Edges with Capacities:\n")
            for u, v in G.edges():
                f.write(f"{u} -> {v} [Capacity: {G[u][v]['capacity']}]\n")
            f.write("</pre></body></html>")
        webbrowser.open(f"file://{tmpfile.name}")


st.title("Max-Flow Algorithms")

st.sidebar.subheader("Graph Controls")
source = st.sidebar.number_input("Source Node", min_value=0, value=st.session_state.source)
sink = st.sidebar.number_input("Sink Node", min_value=0, value=st.session_state.sink)
st.session_state.source, st.session_state.sink = source, sink

st.sidebar.subheader("Upload Graph")
uploaded_file = st.sidebar.file_uploader("Upload a TXT file (u v capacity)", type=["txt"])
if uploaded_file:
    upload_graph(uploaded_file)


u = st.sidebar.number_input("From Node", min_value=0)
v = st.sidebar.number_input("To Node", min_value=0)
capacity = st.sidebar.number_input("Capacity", min_value=1, value=10)
if st.sidebar.button("Add Edge"):
    add_edge(u, v, capacity)


if st.sidebar.button("Remove Edge"):
    remove_edge(u, v)


n = st.sidebar.number_input("Nodes", min_value=2, value=6)
m = st.sidebar.number_input(
    "Edges",
    min_value=max(n-1, 1),  
    value=max(8, n-1)      
)
if st.sidebar.button("Generate Random Graph"):
    generate_random_graph(n, m)

if st.sidebar.button("Save Graph to Neo4j"):
    save_graph_to_neo4j()

graph_id_input = st.sidebar.text_input("Enter Graph ID")

if st.sidebar.button("Save Graph to Neo4j", key="save_graph"):
    save_graph_to_neo4j(graph_id_input)

if st.sidebar.button("Load Graph from Neo4j", key="load_graph"):
    load_graph_from_neo4j(graph_id_input)

if st.button("Run Ford-Fulkerson"):
    run_ford_fulkerson()
if st.button("Run Dinic’s Algorithm"):
    run_dinic()
if st.button("Run Push-Relabel"):
    run_push_relabel()
if st.button("Calculate Minimum Cut"):
    calculate_min_cut()

if st.button("Open Graph in New Tab"):
    open_graph_new_tab()


if st.session_state.graph.number_of_edges() > 0:
    visualize_graph(st.session_state.graph)
else:
    st.warning("No edges available in the graph.")
