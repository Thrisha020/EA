
"""
FINAL

Enterprise Analysis
Author:Thrisha M
date:29th jan

"""

import os
import requests
import subprocess
import json
from bokeh.io import show, save
from bokeh.plotting import figure, from_networkx
from bokeh.models import HoverTool, MultiLine
import networkx as nx
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import networkx as nx
import os
import json
import math
from bokeh.plotting import figure, save, show
from bokeh.models import MultiLine, HoverTool, LabelSet, ColumnDataSource
from bokeh.io import output_file
from bokeh.plotting.graph import from_networkx
import math
import json
import os
import networkx as nx

from bokeh.plotting import figure, show, save, from_networkx
from bokeh.models import (
    Circle,
    MultiLine,
    HoverTool,
    LabelSet,
    ColumnDataSource,
)



def get_object_id(file_path):
    """
    Step 1: Get the object ID by replacing the file path in the API request.
    """
    url = "http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectByPath"
    params = {"path": file_path}
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
    current_dir = os.getcwd()  
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

        elif dep['type'] == "COBOL":
            open_copybook_in_vscode(dep['name'])
        


# def visualize_dependencies(object_name, dependencies):
#     """
#     Visualize dependencies as a graph using Bokeh and capture the URL.
#     """
#     # Create a directed graph
#     graph = nx.DiGraph()
#     graph.add_node(object_name)  # Add the main object as a node

#     # Add edges from the main object to its dependencies
#     for dep in dependencies:
#         graph.add_edge(object_name, dep['name'])

#     # Create a Bokeh plot
#     plot = figure(title="Dependency Graph", x_range=(-2, 2), y_range=(-2, 2),
#                   tools="pan,wheel_zoom,reset", active_scroll="wheel_zoom",
#                   background_fill_color="#f7f9fc", border_fill_color="#ffffff")
#     plot.title.text_font_size = "18pt"
#     plot.title.align = "center"
#     plot.grid.grid_line_color = "lightgray"

#     # Convert the NetworkX graph to a Bokeh graph
#     bokeh_graph = from_networkx(graph, nx.spring_layout, scale=1.5, center=(0, 0))
#     bokeh_graph.node_renderer.data_source.data["node_label"] = list(graph.nodes)

#     # Customize node colors and sizes
#     node_colors = ["#87ceeb" if node == object_name else "#ffcccb" for node in graph.nodes]
#     node_sizes = [50 if node == object_name else 40 for node in graph.nodes]

#     bokeh_graph.node_renderer.data_source.data["fill_color"] = node_colors
#     bokeh_graph.node_renderer.data_source.data["size"] = node_sizes

#     bokeh_graph.node_renderer.glyph.fill_color = "fill_color"
#     bokeh_graph.node_renderer.glyph.line_color = "black"
#     bokeh_graph.node_renderer.glyph.line_width = 1.5
#     bokeh_graph.node_renderer.glyph.size = "size"

#     # Customize edge appearance
#     bokeh_graph.edge_renderer.glyph = MultiLine(line_color="#a3a3a3", line_alpha=0.8, line_width=2)

#     # Add hover tool
#     hover_tool = HoverTool(tooltips=[("Node", "@node_label")])
#     plot.add_tools(hover_tool)

#     # Add the graph to the plot
#     plot.renderers.append(bokeh_graph)

#     # Hide axes and outline
#     plot.xaxis.visible = False
#     plot.yaxis.visible = False
#     plot.outline_line_color = None

#     # Save the plot to an HTML file and get the file path
#     output_file = "dependency_graph.html"
#     save(plot, filename=output_file)

#     # Print the URL in JSON format
#     url = f"file://{os.path.abspath(output_file)}"
#     print(json.dumps({"plot_url": url}, indent=4))

#     # Open the plot in the default web browser
#     show(plot)
def visualize_dependencies(object_name, dependencies):
    """
    Visualize dependencies as a graph using Bokeh and capture the URL.
    """
    # Create a directed graph
    graph = nx.DiGraph()
    graph.add_node(object_name)  # Add the main object as a node

    # Add edges from the main object to its dependencies
    for dep in dependencies:
        graph.add_edge(object_name, dep['name'])

    # Create a Bokeh plot
    plot = figure(title="Dependency Graph", x_range=(-2, 2), y_range=(-2, 2),
                  tools="pan,wheel_zoom,reset", active_scroll="wheel_zoom",
                  background_fill_color="#f7f9fc", border_fill_color="#ffffff")
    plot.title.text_font_size = "12pt"
    plot.title.align = "center"
    #plot.grid.grid_line_color = "lightgray"
    plot.background_fill_color = "LightBlue"

    # Use NetworkX to compute the layout positions for the graph
    pos = nx.spring_layout(graph, scale=1.5, center=(0, 0))

    # Convert the NetworkX graph to a Bokeh graph using the computed positions
    bokeh_graph = from_networkx(graph, pos)
    bokeh_graph.node_renderer.data_source.data["node_label"] = list(graph.nodes)

    # Customize node colors and sizes
    node_colors = ["#87ceeb" if node == object_name else "#ffcccb" for node in graph.nodes]
    node_sizes = [80 if node == object_name else 70 for node in graph.nodes]

    bokeh_graph.node_renderer.data_source.data["fill_color"] = node_colors
    bokeh_graph.node_renderer.data_source.data["size"] = node_sizes

    bokeh_graph.node_renderer.glyph.fill_color = "fill_color"
    bokeh_graph.node_renderer.glyph.line_color = "black"
    bokeh_graph.node_renderer.glyph.line_width = 2
    bokeh_graph.node_renderer.glyph.size = "size"

    # Customize edge appearance
    bokeh_graph.edge_renderer.glyph = MultiLine(line_color="#a3a3a3", line_alpha=0.9, line_width=3)

    # Add hover tool
    hover_tool = HoverTool(tooltips=[("Node", "@node_label")])
    plot.add_tools(hover_tool)

    # Add the graph to the plot
    plot.renderers.append(bokeh_graph)

    # Add text labels to the nodes
    from bokeh.models import ColumnDataSource, LabelSet

    # Extract node positions from the layout
    x_coords = [pos[node][0] for node in graph.nodes]  # X-coordinates of nodes
    y_coords = [pos[node][1] for node in graph.nodes]  # Y-coordinates of nodes
    labels = list(graph.nodes)  # Node labels

    # Create a ColumnDataSource for the labels
    labels_source = ColumnDataSource(data=dict(
        x=x_coords,
        y=y_coords,
        labels=labels
    ))

    # Add labels to the plot
    labels = LabelSet(x='x', y='y', text='labels', source=labels_source,
                      text_font_size="12pt", text_color="#333333",
                      text_align="center", text_baseline="middle")
    plot.add_layout(labels)

    # Hide axes and outline
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.outline_line_color = None

    # Save the plot to an HTML file and get the file path
    output_file = "dependency_graph.html"
    save(plot, filename=output_file)

    # Print the URL in JSON format
    url = f"file://{os.path.abspath(output_file)}"
    print(json.dumps({"plot_url": url}, indent=4))

    # Open the plot in the default web browser
    show(plot)

def get_base_path(file_name):
    """
    Determine the base path based on the file extension.
    """
    # Define the base directories
    cobol_base_path = r"C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\Banking_Demo_Sources\cobol"
    copybook_base_path = r"C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\Banking_Demo_Sources\copybook"

    # Check the file extension
    if file_name.lower().endswith((".cbl", ".cobol")):
        return cobol_base_path
    elif file_name.lower().endswith(".cpy"):
        return copybook_base_path
    else:
        raise ValueError("Unsupported file type. Please provide a COBOL (.cbl, .cobol) or copybook (.cpy) file.")





def visualize_dependencies12(object_name, dependencies):
    """
    Visualize dependencies as a graph using Bokeh and serve the HTML file over HTTP.
    Uses Kamada-Kawai algorithm for better node positioning with minimal overlap.
    """
    # Create a directed graph
    graph = nx.DiGraph()
    graph.add_node(object_name)  # Add the main object as a node

    # Add edges from the main object to its dependencies
    for dep in dependencies:
        graph.add_edge(object_name, dep['name'])

    # Create a Bokeh plot with more space
    plot = figure(title="Dependency Graph", 
                  width=1000, height=1000,  # Larger plot size
                  x_range=(-6, 6), y_range=(-6, 6),  # Wider ranges
                  tools="pan,wheel_zoom,reset,save", 
                  active_scroll="wheel_zoom")
    plot.title.text_font_size = "16pt"
    plot.title.align = "center"
    plot.background_fill_color = "lightgrey"

    # Get the number of dependencies
    num_dependencies = len(dependencies)
    
    # Create a custom circular layout
    pos = {}
    
    # Place the main object in the center
    pos[object_name] = (0, 0)
    
    # Place dependencies in a circle around the main object
    radius = 4  # Adjust radius based on number of nodes
    
    # Calculate positions for the dependencies in a circular layout
    for i, dep in enumerate(dependencies):
        angle = 2 * math.pi * i / num_dependencies
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        pos[dep['name']] = (x, y)
    
    # Convert the NetworkX graph to a Bokeh graph
    bokeh_graph = from_networkx(graph, pos)
    bokeh_graph.node_renderer.data_source.data["node_label"] = list(graph.nodes)

    # Customize node colors and sizes
    node_colors = ["#87ceeb" if node == object_name else "#ffcccb" for node in graph.nodes]
    node_sizes = [100 if node == object_name else 80 for node in graph.nodes]

    bokeh_graph.node_renderer.data_source.data["fill_color"] = node_colors
    bokeh_graph.node_renderer.data_source.data["size"] = node_sizes

    bokeh_graph.node_renderer.glyph.fill_color = "fill_color"
    bokeh_graph.node_renderer.glyph.line_color = "black"
    bokeh_graph.node_renderer.glyph.line_width = 2
    bokeh_graph.node_renderer.glyph.size = "size"

    # Customize edge appearance
    bokeh_graph.edge_renderer.glyph = MultiLine(line_color="#a3a3a3", line_alpha=0.8, line_width=2)

    # Add hover tool
    hover_tool = HoverTool(tooltips=[("Node", "@node_label")])
    plot.add_tools(hover_tool)

    # Add the graph to the plot
    plot.renderers.append(bokeh_graph)

    # Add text labels to the nodes with slight offset from nodes for better readability
    x_coords = []
    y_coords = []
    labels = []
    
    # Calculate label positions with a slight offset
    for node in graph.nodes:
        x, y = pos[node]
        # For dependency nodes, slightly increase the offset in the direction from center
        if node != object_name:
            # Normalize direction vector
            dist = math.sqrt(x*x + y*y)
            if dist > 0:
                # Add a slight offset in the same direction
                offset_factor = 1.15  # 15% further out than the node
                x = x * offset_factor
                y = y * offset_factor
        
        x_coords.append(x)
        y_coords.append(y)
        labels.append(node)

    labels_source = ColumnDataSource(data=dict(
        x=x_coords,
        y=y_coords,
        labels=labels
    ))

    label_set = LabelSet(x='x', y='y', text='labels', source=labels_source,
                          text_font_size="10pt", text_color="#333333",
                          text_align="center", text_baseline="middle")
    plot.add_layout(label_set)

    # Hide axes and outline
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.outline_line_color = None
    plot.grid.visible = False
    # Save the plot to an HTML file
    import os
    
    # Create directory for output if it doesn't exist
    output_file = "dependency_graph.html"
    save(plot, filename=output_file)

    # Print the URL in JSON format
    url = f"file://{os.path.abspath(output_file)}"
    print(json.dumps({"plot_url": url}, indent=4))

    # Open the plot in the default web browser
    show(plot)


def visualize_dependencies123(object_name, dependencies):
    """
    Visualize dependencies as a graph using Bokeh with modern clean design.
    Features curved dotted lines, capsule-shaped nodes, and better color scheme.
    """
    import os
    import math
    import json
    import networkx as nx
    from bokeh.plotting import figure, show, save
    from bokeh.models import ColumnDataSource, LabelSet, MultiLine, HoverTool
    from bokeh.models import Arrow, VeeHead, Circle
    import numpy as np

    # Create a directed graph
    graph = nx.DiGraph()
    graph.add_node(object_name)

    # Add edges from the main object to its dependencies
    for dep in dependencies:
        graph.add_edge(object_name, dep['name'])

    # Create a clean Bokeh plot
    plot = figure(title="Topology example", 
                  width=1200, height=800,
                  x_range=(-7, 7), y_range=(-5, 5),
                  tools="pan,wheel_zoom,reset,save", 
                  active_scroll="wheel_zoom")
    
    # Clean styling
    plot.title.text_font_size = "18pt"
    plot.title.align = "left"
    plot.title.text_color = "#333333"
    plot.background_fill_color = "white"
    plot.border_fill_color = "white"

    # Get the number of dependencies
    num_dependencies = len(dependencies)

    # Create a better circular layout with more spacing
    pos = {}
    pos[object_name] = (0, 0)  # Center position for main object
    
    if num_dependencies > 0:
        radius = 3.5  # Increased radius for better spacing
        
        for i, dep in enumerate(dependencies):
            angle = 2 * math.pi * i / num_dependencies
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            pos[dep['name']] = (x, y)

    # Extract node info for rendering
    x_coords, y_coords, labels, colors, widths, heights = [], [], [], [], [], []
    
    for node in graph.nodes:
        x, y = pos[node]
        label = node.replace("\u2022", "").strip()
        x_coords.append(x)
        y_coords.append(y)
        labels.append(label)

        # Modern color scheme matching the image
        if node == object_name:
            colors.append("#A56EFF33")  # Purple for main nodes
        else:
            colors.append("#3DDBD933")  # Cyan for copybook files
      

        # Dynamic width based on text length for capsule shape
        text_len = len(label)
        widths.append(max(2.8, text_len * 0.18))  # Width for capsule
        heights.append(0.8)  # Height for capsule

    # Create data source for nodes
    source = ColumnDataSource(data=dict(
        x=x_coords,
        y=y_coords,
        labels=labels,
        fill_color=colors,
        width=widths,
        height=heights
    ))

    # Draw capsule-shaped nodes using ellipse (oval) method
    plot.ellipse(x="x", y="y", width="width", height="height",
                 fill_color="fill_color", 
                 line_color="white", 
                 line_width=2,
                 fill_alpha=0.9,
                 source=source)

    # Add clean labels (removed text_font_weight)
    label_set = LabelSet(x="x", y="y", text="labels", source=source,
                         text_font_size="11pt", 
                         text_color="black",
                         text_align="center", 
                         text_baseline="middle",
                         text_font_style="normal")
    plot.add_layout(label_set)

    # Add modern hover tool
    hover_tool = HoverTool(tooltips=[
        ("Node", "@labels"),
        ("Type", "Dependency")
    ])
    plot.add_tools(hover_tool)

    # Create curved dotted lines for edges
    def create_curved_line(start, end, num_points=50):
        """Create a smooth curved line between two points"""
        x0, y0 = start
        x1, y1 = end
        
        # Calculate control point for curve
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        
        # Add curvature perpendicular to the line
        dx = x1 - x0
        dy = y1 - y0
        length = math.sqrt(dx**2 + dy**2)
        
        if length > 0:
            # Normalize and rotate 90 degrees
            perp_x = -dy / length
            perp_y = dx / length
            
            # Add curve offset
            curve_strength = 0.8
            ctrl_x = mid_x + perp_x * curve_strength
            ctrl_y = mid_y + perp_y * curve_strength
        else:
            ctrl_x, ctrl_y = mid_x, mid_y

        # Create quadratic bezier curve
        t = np.linspace(0, 1, num_points)
        curve_x = (1-t)**2 * x0 + 2*(1-t)*t * ctrl_x + t**2 * x1
        curve_y = (1-t)**2 * y0 + 2*(1-t)*t * ctrl_y + t**2 * y1
        
        return curve_x.tolist(), curve_y.tolist()

    # Draw curved edges
    for start_node, end_node in graph.edges:
        start_pos = pos[start_node]
        end_pos = pos[end_node]
        
        curve_x, curve_y = create_curved_line(start_pos, end_pos)
        
        # Draw the curved line
        plot.line(curve_x, curve_y, 
                 line_color="#9CA3AF", 
                 line_alpha=0.7, 
                 line_width=2, 
                 line_dash=[8, 4])  # Dotted line pattern

    # Add small dots along the edges for better visual effect
    for start_node, end_node in graph.edges:
        start_pos = pos[start_node]
        end_pos = pos[end_node]
        
        curve_x, curve_y = create_curved_line(start_pos, end_pos, 15)
        
        # Add small dots along the curve
        dot_indices = [3, 7, 11]  # Select specific points for dots
        for i in dot_indices:
            if i < len(curve_x):
                plot.circle(curve_x[i], curve_y[i], 
                           size=4, 
                           color="#9CA3AF", 
                           alpha=0.6)

    # Add special annotation for copybook usage (like in the image)
    if object_name.endswith(".cbl"):
        # Find a .cpy dependency to annotate
        cpy_deps = [dep for dep in dependencies if dep['name'].endswith('.cpy')]
        if cpy_deps:
            cpy_pos = pos[cpy_deps[0]['name']]
            plot.text([cpy_pos[0] - 1.5], [cpy_pos[1] + 0.8], 
                     text=["Use copybook"], 
                     text_color="#8B5CF6", 
                     text_font_size="10pt",
                     text_font_style="italic")

    # Clean up the plot appearance
    plot.xaxis.visible = False
    plot.yaxis.visible = False
    plot.outline_line_color = None
    plot.grid.visible = False
    plot.toolbar.logo = None

    # Save and display
    output_file = "dependency_graph.html"
    save(plot, filename=output_file)

    # Print the URL in JSON format
    url = f"file://{os.path.abspath(output_file)}"
    print(json.dumps({"plot_url": url}, indent=4))

    # Open the plot in the default web browser
    show(plot)
# from pyvis.network import Network

# def visualize_pyvis_graph(object_name, dependencies):
#     """
#     Visualize 2-layer capsule-shaped dependency graph using pyvis.
#     """
#     net = Network(height="800px", width="100%", directed=True, bgcolor="#d0ecf0", font_color="black")

#     # Configure physics and layout
#     net.barnes_hut()
#     net.set_options("""
#     var options = {
#       "nodes": {
#         "shape": "box",
#         "borderRadius": 15,
#         "font": {
#           "align": "center"
#         }
#       },
#       "edges": {
#         "smooth": true,
#         "arrows": {
#           "to": {
#             "enabled": true
#           }
#         }
#       },
#       "layout": {
#         "improvedLayout": true
#       },
#       "physics": {
#         "stabilization": {
#           "enabled": true
#         }
#       }
#     }
#     """)

#     # Add the central node (.cpy)
#     net.add_node(
#         object_name,
#         label=object_name,
#         color="#91d5ff",  # light blue
#         shape="box",
#         borderWidth=2
#     )

#     # Add dependencies (.cbl files)
#     for dep in dependencies:
#         dep_name = dep['name']
#         relation = dep.get("relation", "")  # Optional: for edge type
#         color = "#f9c0c0" if dep_name.endswith(".cbl") else "#d3d3d3"

#         net.add_node(
#             dep_name,
#             label=dep_name,
#             color=color,
#             shape="box",
#             borderWidth=1
#         )

#         edge_style = "dashed" if relation == "Use copybook" else "solid"

#         net.add_edge(
#             object_name,
#             dep_name,
#             color="gray",
#             dashes=(edge_style == "dashed")
#         )

#     # Generate and show
#     output_path = "capsule_dependency_graph.html"
#     net.show(output_path)
#     print(f"Graph saved to: {output_path}")






def main():
    # Ask the user for the COBOL file name
    file_name = input("Please enter the COBOL file name: ")

    # Determine the base path based on the file extension
    try:
        base_path = get_base_path(file_name)
    except ValueError as e:
        print(e)
        return

    # Construct the full file path
    file_path = os.path.join(base_path, file_name)
    file_path = os.path.normpath(file_path)
    file_path = file_path.replace("/", "\\")

    print(f"Constructed file path: {file_path}")

    # Fetch the object ID and name
    print(f"Fetching object ID for the given file '{file_name}'...")
    object_id, object_name = get_object_id(file_path)

    if object_id:
        print(f"Object ID retrieved: {object_id}")
        print("Fetching dependencies...")

        # Fetch the dependencies
        dependencies = get_dependencies(object_id)
        print(f'\n dep b4 removal:   {dependencies}')
        dependencies = [dep for dep in dependencies if dep['name']!=file_name.split('.')[0]]
        print(f'\n dep after removal:   {dependencies}')
        if dependencies:
            display_dependencies(dependencies, base_path)
            #visualize_dependencies(object_name, dependencies)
            visualize_dependencies123(object_name, dependencies)
            #visualize_dependencies(object_name, dependencies)

        else:
            print("No dependencies found.")
    else:
        print("Failed to retrieve object ID.")

if __name__ == "__main__":
    main()
    #open_copybook_in_vscode('epsmlis.cpy')



# SBANK00P.cbl

# 172.17.64.4:1248

# MBANKZZ.cpy

# DFHAID.CPY

# CBANKDAT.cpy