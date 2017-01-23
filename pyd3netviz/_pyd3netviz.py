# -*- coding: utf-8 -*-
"""
@author: Bob Baxley
"""
# Wrapper for showing d3 force layout visualization in python
#
# Acknowledgements and more information
# See https://bl.ocks.org/mbostock/4062045
# Inspiration and template for package comes from
# https://github.com/hmelberg/motionchart

from os.path import join, dirname, abspath
import webbrowser
import json
import pyperclip
from networkx.readwrite import json_graph
from IPython.display import IFrame, display


def _add_file_to_path(path):
    return 'file://' + path


def _get_js(file_name):
    this_path = dirname(__file__)
    file_path = join(this_path, 'js', file_name)
    with open(file_path) as f_handle:
        out = f_handle.read()
    return out


class ForceChart(object):
    ''' Create a force chart
    '''

    def __init__(self,
                 graph_data,
                 link_distance=200, charge=-1000,
                 node_radius=5, stroke_width=1
                 ):
        d3_raw = _get_js('d3.min.js')
        fl_raw = _get_js('force_layout.js')

        variables = """
           graph={};
           link_distance={};
           charge={};
           node_radius={};
           stroke_width={};
           """.format(json.dumps(json_graph.node_link_data(graph_data)),
                      link_distance,
                      charge,
                      node_radius,
                      stroke_width)


        self.template = '''<!DOCTYPE html><html><head>
        </head><body>
        <div id="chart1"></div>
        <script>
        {d3_raw}
        {variables}
        {fl_raw}
        </script>
        <script>
        draw_graph(graph,link_distance,charge,node_radius,stroke_width);
        </script></body></html>
        '''.format(d3_raw=d3_raw, fl_raw=fl_raw, variables=variables)

    def to_browser(self, path_and_name):
        """Open vis in browser."""
        path = self.to_file(path_and_name)
        url = _add_file_to_path(path)
        webbrowser.open(url)

    def _repr_html_(self):
        """return the embed iframe"""
        return self.template

    def to_notebook(self, path_and_name='temp.html', width=900, height=700):
        """open viz in notebook cell"""

        self.to_file(path_and_name)

        display(IFrame(src=path_and_name, width=width, height=height))

    def to_clipboard(self):
        """ send viz to clipboard """
        pyperclip.copy(self.template)

    def to_file(self, path_and_name):
        """ send viz to file """
        path = abspath(path_and_name)

        with open(path, 'w') as f_handle:
            f_handle.write(self.template)
        return path


def demo():
    """Demo in notebook"""
    pass