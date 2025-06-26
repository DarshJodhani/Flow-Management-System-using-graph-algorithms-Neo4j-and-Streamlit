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

🔧 Installation & Setup
Step 1: Clone the Repository

git clone https://github.com/DarshJodhani/Flow-Management-System-using-graph-algorithms-Neo4j-and-Streamlit.git
cd Flow-Management-System-using-graph-algorithms-Neo4j-and-Streamlit

📁 Flow-Management-System...
├── GT Assignment Report.docx
├── Max-flow_algos.py         ← Main Streamlit app
├── README.md
├── dd.txt                    ← Sample graph file (u v capacity)
├── dinics.py                ← Optional Dinic’s implementation
├── ford.py                  ← Optional Ford-Fulkerson
├── pushrelabel.py           ← Optional Push-Relabel

Step 2: Install Dependencies
Install required packages:

streamlit
networkx
matplotlib
neo4j

Before running make sure that you have added neo4j uri,user,password into code.

Step 3: Run the Application
streamlit run Max-flow_algos.py

📁 Graph Upload Format
Upload .txt files using the format:
<from_node> <to_node> <capacity>
Example:
0 1 10
1 2 5
2 3 7

🧪 Testing & Visualization

View graphs in real time with Streamlit and Matplotlib
Run flow algorithms and display results with execution time
Compute minimum cut and display edges involved
Open a full graph report in a new browser tab

📤 Save/Load Graphs (Neo4j)

Save graphs with a Graph ID
Load any saved graph later using the same ID
Neo4j schema:
(:Node {id, graph_id})
[:FLOW {capacity, graph_id}]

