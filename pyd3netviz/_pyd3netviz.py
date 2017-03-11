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
    """ get the code in a javascript file """
    this_path = dirname(__file__)
    file_path = join(this_path, 'js', file_name)
    with open(file_path) as f_handle:
        out = f_handle.read()
    return out


class ForceChart(object):
    ''' Create a force chart
    '''
    variable_template = """
            graph={graph};
            height={height};
            width={width};
            link_distance={link_distance};
            charge={charge};
            default_link_color="{default_link_color}";
            default_link_opacity={default_link_opacity};
            default_link_width={default_link_width};
            default_node_radius={default_node_radius};
            default_node_color="{default_node_color}";
            default_node_opacity={default_node_opacity};
            link_color_field="{link_color_field}";
            link_opacity_field="{link_opacity_field}";
            link_width_field="{link_width_field}";
            node_radius_field="{node_radius_field}";
            node_color_field="{node_color_field}";
            node_opacity_field="{node_opacity_field}";
           """

    html_template = """
        <!DOCTYPE html><html><head>
        </head><body style="
                    margin: 0px;
                    overflow: hidden;
                ">
        <div id="chart1"></div>
        <script>
        {d3_raw}
        {variables}
        {fl_raw}
        </script>
        <script>
        draw_graph(graph,
            link_distance, charge,
            width, height,
            default_link_color, default_link_opacity, default_link_width,
            default_node_radius, default_node_color, default_node_opacity,
            link_color_field, link_opacity_field, link_width_field,
            node_radius_field, node_color_field, node_opacity_field);
        </script></body></html>
       """

    def __init__(self,
                 graph_data,
                 link_distance=10, charge=-100,
                 width=960, height=600,
                 default_link_color='#900',
                 default_link_opacity=.5,
                 default_link_width=5,
                 default_node_radius=10,
                 default_node_color='#999',
                 default_node_opacity=.5,
                 link_color_field=None,
                 link_opacity_field=None,
                 link_width_field=None,
                 node_radius_field=None,
                 node_color_field=None,
                 node_opacity_field=None):
        d3_raw = _get_js('d3.min.js')
        fl_raw = _get_js('force_layout.js')
        self.width = width
        self.height = height

        # assumes `None` is not a field.
        # todo: more elegant way to handle this
        variables = self.variable_template.format(
            graph=json.dumps(json_graph.node_link_data(graph_data)),
            width=width, height=height,
            link_distance=link_distance,
            charge=charge,
            default_link_color=default_link_color,
            default_link_opacity=default_link_opacity,
            default_link_width=default_link_width,
            default_node_radius=default_node_radius,
            default_node_color=default_node_color,
            default_node_opacity=default_node_opacity,
            link_color_field=link_color_field,
            link_opacity_field=link_opacity_field,
            link_width_field=link_width_field,
            node_radius_field=node_radius_field,
            node_color_field=node_color_field,
            node_opacity_field=node_opacity_field)

        self.html = self.html_template.format(
            d3_raw=d3_raw, fl_raw=fl_raw, variables=variables)

    def to_browser(self, path_and_name):
        """Open vis in browser."""
        path = self.to_file(path_and_name)
        url = _add_file_to_path(path)
        webbrowser.open(url)

    def to_notebook(self, path_and_name='temp.html', width=None, height=None):
        """open viz in notebook cell"""

        self.to_file(path_and_name)

        display(IFrame(src=path_and_name,
                       width=self.width if width is None else width,
                       height=self.height if height is None else height))

    def to_clipboard(self):
        """ send viz to clipboard """
        pyperclip.copy(self.html)

    def to_file(self, path_and_name):
        """ send viz to file """
        path = abspath(path_and_name)

        with open(path, 'w') as f_handle:
            f_handle.write(self.html)
        return path


def demo():
    """Demo in notebook"""
    pass