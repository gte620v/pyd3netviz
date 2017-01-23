// From https://bl.ocks.org/mbostock/4062045
// Copyright Mike Bostock
// Released under the GNU General Public License, version 3.

function draw_graph(graph, link_distance, charge, node_radius, stroke_width) {

    var margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 40
    };
    var width = 960 - margin.left - margin.right;
    var height = 600 - margin.top - margin.bottom;
    var svg = d3.select("#chart1").append("svg")
        .style("position", "relative")
        .style("max-width", "960px")
        .attr("width", width + "px")
        .attr("height", (height + 50) + "px")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var color = d3.scale.category10();
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
            return d.d3color;
        })
        .style("stroke-opacity", .5)
        .style("stroke-width", stroke_width);


    var node = svg.selectAll("circle.node")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", node_radius)
        .style("fill", "#999")
        .style("opacity", .4)
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
