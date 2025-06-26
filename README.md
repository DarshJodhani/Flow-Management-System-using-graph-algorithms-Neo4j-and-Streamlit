# Flow-Management-System-using-graph-algorithms-Neo4j-and-Streamlit

An interactive web application to simulate Max-Flow algorithms (Ford-Fulkerson, Dinic’s, and Push-Relabel) on directed graphs, with persistent storage using Neo4j and a UI powered by Streamlit.

consider only Max-flow_algos.py for code, dd.txt for example, report for workflow.

📌 Features
🎯 Run Max-Flow Algorithms: Ford-Fulkerson, Dinic’s Algorithm, and Push-Relabel.
🧩 Interactive Graph Editing: Add/remove edges, define capacities via UI.
🔀 Random Graph Generation: Generate connected graphs with specified nodes and edges.
📤 Upload Graph: Upload from a .txt file (format: u v capacity).
💾 Persistent Storage: Save/load graphs using Neo4j with a unique Graph ID.
🌐 Graph Viewer: Open graph details in a separate browser tab.
📊 Minimum Cut: View cut value and edges involved.

🔧 Tech Stack
Python
Streamlit – UI framework
NetworkX – Graph algorithms and structure
Neo4j – Graph database for persistent storage
Matplotlib – Graph visualization
webbrowser / tempfile – For opening graph info externally

