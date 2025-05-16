from bokeh.models import CustomJS, TapTool, ColumnDataSource

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
import os
import requests
import subprocess
import json
import networkx as nx
from bokeh.io import show, save
from bokeh.plotting import figure, from_networkx
from bokeh.models import HoverTool, MultiLine, Button, CustomJS
from bokeh.events import ButtonClick
from functools import partial

def visualize_dependencies(object_name, dependencies):
    """Visualize dependencies as a graph using Bokeh with clickable nodes."""
    
    # Create a directed graph
    graph = nx.DiGraph()
    graph.add_node(object_name)  # Add the main object as a node

    # Add edges from the main object to its dependencies
    for dep in dependencies:
        graph.add_edge(object_name, dep['name'])

    # Create a Bokeh plot
    plot = figure(title="Dependency Graph", tools="pan,wheel_zoom,reset,tap", 
                  active_scroll="wheel_zoom", background_fill_color="#f7f9fc")

    pos = nx.spring_layout(graph, scale=1.5, center=(0, 0))
    bokeh_graph = from_networkx(graph, pos)

    # Add labels to nodes
    node_labels = list(graph.nodes)
    bokeh_graph.node_renderer.data_source.data["node_label"] = node_labels

    # Define colors and sizes
    node_colors = ["#87ceeb" if node == object_name else "#ffcccb" for node in graph.nodes]
    node_sizes = [80 if node == object_name else 70 for node in graph.nodes]

    bokeh_graph.node_renderer.data_source.data["fill_color"] = node_colors
    bokeh_graph.node_renderer.data_source.data["size"] = node_sizes

    bokeh_graph.node_renderer.glyph.fill_color = "fill_color"
    bokeh_graph.node_renderer.glyph.size = "size"

    # Create a TapTool with CustomJS callback
    callback = CustomJS(args=dict(source=bokeh_graph.node_renderer.data_source), code="""
        var selected = source.selected.indices;
        if (selected.length > 0) {
            var nodeName = source.data['node_label'][selected[0]];
            console.log("Clicked node:", nodeName);
            fetch('/api/clicked_node', {
                method: 'POST',
                body: JSON.stringify({node: nodeName}),
                headers: {'Content-Type': 'application/json'}
            }).then(response => response.json()).then(data => console.log(data));
        }
    """)

    tap_tool = TapTool(callback=callback)
    plot.add_tools(tap_tool)

    # Save and display the plot
    output_file = "dependency_graph.html"
    save(plot, filename=output_file)
    show(plot)
