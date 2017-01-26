// From https://bl.ocks.org/mbostock/4062045
// Copyright Mike Bostock
// Released under the GNU General Public License, version 3.


function get_val(d, field, default_val) {
    if (field in d) {
        return d[field];
    } else {
        return default_val;
    }
}

function draw_graph(graph,
    link_distance, charge,
    width, height,
    default_link_color, default_link_opacity, default_link_width,
    default_node_radius, default_node_color, default_node_opacity,
    link_color_field, link_opacity_field, link_width_field,
    node_radius_field, node_color_field, node_opacity_field) {

    var svg = d3.select("#chart1").append("svg")
        .style("position", "relative")
        .style("max-width", width + "px")
        .attr("width", width + "px")
        .attr("height", height + "px")
        .append("g");


    var force = d3.layout.force()
        .charge(charge)
        .linkDistance(link_distance)
        .size([width, height]);

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var link = svg.selectAll("line.link")
        .data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke", function(d) {
            return get_val(d, link_color_field, default_link_color);
        })
        .style("stroke-opacity", function(d) {
            return get_val(d, link_opacity_field, default_link_opacity);
        })
        .style("stroke-width", function(d) {
            return get_val(d, link_width_field, default_link_width);
        });


    var node = svg.selectAll("circle.node")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", function(d) {
            return get_val(d, node_radius_field, default_node_radius);
        })
        .style("fill", function(d) {
            return get_val(d, node_color_field, default_node_color);
        })
        .style("opacity", function(d) {
            return get_val(d, node_opacity_field, default_node_opacity);
        })
        .call(force.drag);

    force.on("tick", function() {
        link.attr("x1", function(d) {
                return d.source.x;
            })
            .attr("y1", function(d) {
                return d.source.y;
            })
            .attr("x2", function(d) {
                return d.target.x;
            })
            .attr("y2", function(d) {
                return d.target.y;
            });
        node.attr("cx", function(d) {
                return d.x;
            })
            .attr("cy", function(d) {
                return d.y;
            });
    });
}
