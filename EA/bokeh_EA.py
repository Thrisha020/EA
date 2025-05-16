import os
import requests
import subprocess
import urllib.parse
from bokeh.io import show
from bokeh.plotting import figure, from_networkx
from bokeh.models import HoverTool, MultiLine
import networkx as nx

def get_object_id(file_path):
    """
    Step 1: Get the object ID by replacing the file path in the API request.
    """
    url = "http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectByPath"
    params = {
        "path": file_path
    }
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        object_id = result.get("id")  # Assuming the response has an 'id' field
        object_name = result.get("name")  # Assuming the response has a 'name' field
        return object_id, object_name
    else:
        print(f"Error getting object ID: {response.status_code}")
        print(response.text)
        return None, None

def get_dependencies(object_id):
    """
    Step 2: Get dependencies by replacing the object ID in the API request.
    """
    url = "http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectDirectRelationship"
    params = {"id": object_id}
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        dependencies = response.json()
        return dependencies
    else:
        print(f"Error getting dependencies: {response.status_code}")
        print(response.text)
        return None

def open_copybook_in_vscode(file_name):
    """
    Open a copybook file in Visual Studio Code by searching in the current working directory and its subdirectories.
    """
    current_dir = os.getcwd()  # Get the current working directory

    # Use os.walk to search through all directories and subdirectories
    for root, dirs, files in os.walk(current_dir):
        if file_name in files:
            file_path = os.path.join(root, file_name)  # Full path to the file
            print(f"Found {file_name} at {file_path}")  # Print where the file was found
            subprocess.run(["code", file_path])  # Open the file in VS Code
            return

    print(f"File {file_name} not found in the current directory or any subdirectory.")

def display_dependencies(dependencies, base_path):
    """
    Step 3: Display dependencies and optionally open copybooks in Visual Studio Code.
    """
    print("Chat: Please find the list of dependency code:")
    for dep in dependencies:
        print(f"{dep['name']} (Type: {dep['type']}, Relation: {dep['relation']})")
       
        if dep['type'] == "COPYBOOK":
            open_copybook_in_vscode(dep['name'])

def visualize_dependencies(object_name, dependencies):
    """
    Visualize dependencies as a graph using Bokeh.
    """
    
    graph = nx.DiGraph()
    graph.add_node(object_name)  


    for dep in dependencies:
        graph.add_edge(object_name, dep['name'])

    
    plot = figure(title="Dependency Graph", x_range=(-2, 2), y_range=(-2, 2),
                  tools="pan,wheel_zoom,reset", active_scroll="wheel_zoom",
                  background_fill_color="#f7f9fc", border_fill_color="#ffffff")
    plot.title.text_font_size = "18pt"
    plot.title.align = "center"
    plot.grid.grid_line_color = "lightgray"


    bokeh_graph = from_networkx(graph, nx.spring_layout, scale=1.5, center=(0, 0))
    bokeh_graph.node_renderer.data_source.data["node_label"] = list(graph.nodes)


    node_colors = ["#87ceeb" if node == object_name else "#ffcccb" for node in graph.nodes]
    node_sizes = [50 if node == object_name else 40 for node in graph.nodes]  # Increased node sizes

    bokeh_graph.node_renderer.data_source.data["fill_color"] = node_colors
    bokeh_graph.node_renderer.data_source.data["size"] = node_sizes

   
    bokeh_graph.node_renderer.glyph.fill_color = "fill_color"
    bokeh_graph.node_renderer.glyph.line_color = "black"
    bokeh_graph.node_renderer.glyph.line_width = 1.5
    bokeh_graph.node_renderer.glyph.size = "size" 

 
    bokeh_graph.edge_renderer.glyph = MultiLine(line_color="#a3a3a3", line_alpha=0.8, line_width=2)

   
    hover_tool = HoverTool(tooltips=[("Node", "@node_label")])
    plot.add_tools(hover_tool)

 
    plot.renderers.append(bokeh_graph)


    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.outline_line_color = None

   
    show(plot)

def main():
    
    base_path = r"C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\Banking_Demo_Sources\cobol"
    

    file_name = input("Please enter the COBOL file name: ")

    file_path = os.path.join(base_path, file_name)
    file_path = os.path.normpath(file_path)
    file_path = file_path.replace("/", "\\")

    print(f"Constructed file path: {file_path}")

    print(f"Fetching object ID for the given file '{file_name}'...")
    object_id, object_name = get_object_id(file_path)

    if object_id:
        print(f"Object ID retrieved: {object_id}")
        print("Fetching dependencies...")

        dependencies = get_dependencies(object_id)
        if dependencies:
            display_dependencies(dependencies, base_path)
            visualize_dependencies(object_name, dependencies)
        else:
            print("No dependencies found.")
    else:
        print("Failed to retrieve object ID.")

if __name__ == "__main__":
    main()
