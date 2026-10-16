// D3 Force-Directed Network Graph Component

export class NetworkGraph {
  constructor(containerSelector, tooltipSelector, options = {}) {
    this.container = d3.select(containerSelector);
    this.tooltip = d3.select(tooltipSelector);
    this.options = options;
    
    this.width = 800;
    this.height = 600;
    this.selectedNode = null;

    this.init();
  }

  init() {
    this.container.selectAll("*").remove();

    this.svg = this.container.append("svg")
      .attr("width", "100%")
      .attr("height", "100%");

    this.g = this.svg.append("g");

    // Setup Zoom & Pan
    this.zoom = d3.zoom()
      .scaleExtent([0.3, 4])
      .on("zoom", (event) => {
        this.g.attr("transform", event.transform);
      });

    this.svg.call(this.zoom).on("dblclick.zoom", null);

    this.linkGroup = this.g.append("g").attr("class", "links");
    this.nodeGroup = this.g.append("g").attr("class", "nodes");

    this.simulation = d3.forceSimulation()
      .force("charge", d3.forceManyBody().strength(-320))
      .force("center", d3.forceCenter(0, 0))
      .force("collide", d3.forceCollide().radius(45));

    this.resize();
    window.addEventListener("resize", () => this.resize());
  }

  resize() {
    const rect = this.container.node().getBoundingClientRect();
    this.width = rect.width || 800;
    this.height = rect.height || 600;

    this.svg.attr("viewBox", [-this.width / 2, -this.height / 2, this.width, this.height]);
    this.simulation.force("center", d3.forceCenter(0, 0));
    this.simulation.alpha(0.2).restart();
  }

  zoomIn() {
    this.svg.transition().duration(300).call(this.zoom.scaleBy, 1.3);
  }

  zoomOut() {
    this.svg.transition().duration(300).call(this.zoom.scaleBy, 0.7);
  }

  resetZoom() {
    this.svg.transition().duration(400).call(this.zoom.transform, d3.zoomIdentity);
  }

  update(graphData) {
    this.nodes = (graphData.nodes || []).map(d => ({ ...d }));
    this.links = (graphData.links || []).map(d => ({
      ...d,
      source: d.source,
      target: d.target
    }));

    const maxStrength = d3.max(this.nodes, d => d.degree_strength) || 1;
    const radiusScale = d3.scaleSqrt().domain([0, maxStrength]).range([16, 36]);
    const colorScale = d3.scaleOrdinal(d3.schemeTableau10);

    // Update force links
    this.simulation.nodes(this.nodes);
    this.simulation.force("link", d3.forceLink(this.links)
      .id(d => d.id)
      .distance(l => Math.max(80, 200 - Math.abs(l.value) * 120))
      .strength(l => Math.abs(l.value) * 0.8)
    );

    this.simulation.alpha(0.8).restart();

    // Render Links
    const linkSel = this.linkGroup.selectAll("line.link")
      .data(this.links, d => `${d.source.id || d.source}-${d.target.id || d.target}`);

    linkSel.exit().remove();

    const linkEnter = linkSel.enter().append("line")
      .attr("class", d => `link ${d.value < 0 ? 'neg-link' : ''}`)
      .attr("stroke-linecap", "round")
      .on("mousemove", (event, d) => {
        const sName = d.source.id || d.source;
        const tName = d.target.id || d.target;
        this.tooltip
          .style("opacity", 1)
          .style("left", `${event.pageX + 15}px`)
          .style("top", `${event.pageY + 10}px`)
          .html(`
            <strong>${sName} ↔ ${tName}</strong><br/>
            Correlation: <b>${d.value > 0 ? '+' : ''}${d.value.toFixed(3)}</b><br/>
            p-value: <b>${d.p_value}</b> (${d.significant ? 'Significant' : 'Not Sig.'})<br/>
            <span style="color:#93c5fd;font-size:11px;">(Click to view scatter plot)</span>
          `);
      })
      .on("mouseleave", () => this.tooltip.style("opacity", 0))
      .on("click", (event, d) => {
        if (this.options.onEdgeClick) {
          const sName = d.source.id || d.source;
          const tName = d.target.id || d.target;
          this.options.onEdgeClick(sName, tName, d);
        }
      });

    const linkMerged = linkEnter.merge(linkSel)
      .attr("stroke", d => d.value >= 0 ? "var(--accent-pos)" : "var(--accent-neg)")
      .attr("stroke-width", d => Math.max(1.5, Math.abs(d.value) * 7))
      .attr("stroke-opacity", 0.65)
      .attr("class", d => `link ${d.value < 0 ? 'neg-link' : ''}`);

    // Render Nodes
    const nodeSel = this.nodeGroup.selectAll("g.node")
      .data(this.nodes, d => d.id);

    nodeSel.exit().remove();

    const nodeEnter = nodeSel.enter().append("g")
      .attr("class", "node")
      .call(d3.drag()
        .on("start", (event, d) => {
          if (!event.active) this.simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on("drag", (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on("end", (event, d) => {
          if (!event.active) this.simulation.alphaTarget(0);
          if (!d.pinned) {
            d.fx = null;
            d.fy = null;
          }
        }))
      .on("dblclick", (event, d) => {
        // Toggle pin
        d.pinned = !d.pinned;
        if (!d.pinned) {
          d.fx = null;
          d.fy = null;
        } else {
          d.fx = d.x;
          d.fy = d.y;
        }
        d3.select(event.currentTarget).classed("pinned", d.pinned);
      })
      .on("click", (event, d) => {
        this.selectedNode = (this.selectedNode === d.id) ? null : d.id;
        this.updateHighlight();
        if (this.options.onNodeClick) {
          this.options.onNodeClick(d, this.selectedNode ? this.getConnectedLinks(d.id) : null);
        }
      });

    nodeEnter.append("circle");
    nodeEnter.append("text").attr("text-anchor", "middle").attr("dy", 4);

    const nodeMerged = nodeEnter.merge(nodeSel);

    nodeMerged.select("circle")
      .attr("r", d => radiusScale(d.degree_strength))
      .attr("fill", (d, i) => colorScale(i));

    nodeMerged.select("text")
      .attr("y", d => radiusScale(d.degree_strength) + 14)
      .text(d => d.name);

    // Simulation tick handler
    this.simulation.on("tick", () => {
      linkMerged
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      nodeMerged.attr("transform", d => `translate(${d.x},${d.y})`);
    });

    this.activeLinks = this.links;
    this.updateHighlight();
  }

  getConnectedLinks(nodeId) {
    return this.links.filter(l => {
      const s = l.source.id || l.source;
      const t = l.target.id || l.target;
      return s === nodeId || t === nodeId;
    });
  }

  updateHighlight() {
    if (!this.selectedNode) {
      this.nodeGroup.selectAll("g.node").classed("dim", false);
      this.linkGroup.selectAll("line.link").classed("dim", false);
      return;
    }

    const sel = this.selectedNode;
    this.nodeGroup.selectAll("g.node")
      .classed("dim", d => {
        if (d.id === sel) return false;
        return !this.links.some(l => {
          const s = l.source.id || l.source;
          const t = l.target.id || l.target;
          return (s === sel && t === d.id) || (t === sel && s === d.id);
        });
      });

    this.linkGroup.selectAll("line.link")
      .classed("dim", d => {
        const s = d.source.id || d.source;
        const t = d.target.id || d.target;
        return s !== sel && t !== sel;
      });
  }

  exportSVG() {
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(this.svg.node());
    const blob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "correlation-network.svg";
    a.click();
    URL.revokeObjectURL(url);
  }
}
