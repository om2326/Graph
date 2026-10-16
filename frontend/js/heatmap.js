// Correlation Heatmap Matrix View

export class CorrelationHeatmap {
  constructor(containerSelector, tooltipSelector, options = {}) {
    this.container = d3.select(containerSelector);
    this.tooltip = d3.select(tooltipSelector);
    this.options = options;
  }

  update(matrixData, columns) {
    this.container.selectAll("*").remove();

    if (!matrixData || !columns || columns.length === 0) {
      this.container.append("div")
        .style("padding", "30px")
        .style("color", "var(--muted)")
        .text("No correlation matrix data available.");
      return;
    }

    const margin = { top: 70, right: 30, bottom: 40, left: 110 };
    const rect = this.container.node().getBoundingClientRect();
    const size = Math.min(rect.width - margin.left - margin.right, rect.height - margin.top - margin.bottom, 620);
    
    const svg = this.container.append("svg")
      .attr("width", size + margin.left + margin.right)
      .attr("height", size + margin.top + margin.bottom)
      .style("display", "block")
      .style("margin", "auto");

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand().range([0, size]).domain(columns).padding(0.05);
    const y = d3.scaleBand().range([0, size]).domain(columns).padding(0.05);

    // Color interpolator: Neg (-1) = #b5452d, 0 = #f8f9fa, Pos (+1) = #1c6e6e
    const colorScale = d3.scaleDiverging()
      .domain([-1, 0, 1])
      .interpolator(d3.interpolateRgbBasis(["#b5452d", "#f8f9fa", "#1c6e6e"]));

    // X Axis
    g.append("g")
      .call(d3.axisTop(x).tickSize(0))
      .selectAll("text")
      .attr("transform", "rotate(-35)")
      .style("text-anchor", "start")
      .style("font-size", "11px")
      .style("font-weight", "600")
      .style("fill", "var(--ink)");

    // Y Axis
    g.append("g")
      .call(d3.axisLeft(y).tickSize(0))
      .selectAll("text")
      .style("font-size", "11px")
      .style("font-weight", "600")
      .style("fill", "var(--ink)");

    // Flatten rows
    const cells = [];
    matrixData.forEach(row => {
      row.forEach(cell => cells.push(cell));
    });

    // Draw Heatmap Cells
    const cellGroups = g.selectAll(".heat-cell-g")
      .data(cells)
      .enter()
      .append("g")
      .attr("class", "heat-cell-g");

    cellGroups.append("rect")
      .attr("class", "heat-cell")
      .attr("x", d => x(d.target))
      .attr("y", d => y(d.source))
      .attr("width", x.bandwidth())
      .attr("height", y.bandwidth())
      .attr("rx", 3)
      .style("fill", d => colorScale(d.r))
      .on("mousemove", (event, d) => {
        this.tooltip
          .style("opacity", 1)
          .style("left", `${event.pageX + 14}px`)
          .style("top", `${event.pageY + 10}px`)
          .html(`
            <strong>${d.source} ↔ ${d.target}</strong><br/>
            Correlation: <b>${d.r > 0 ? '+' : ''}${d.r.toFixed(3)}</b><br/>
            p-value: <b>${d.p}</b><br/>
            <span style="color:#93c5fd;font-size:11px;">(Click cell to open scatter plot)</span>
          `);
      })
      .on("mouseleave", () => this.tooltip.style("opacity", 0))
      .on("click", (event, d) => {
        if (d.source !== d.target && this.options.onCellClick) {
          this.options.onCellClick(d.source, d.target, d);
        }
      });

    // Cell Text Values if space allows
    if (x.bandwidth() > 32) {
      cellGroups.append("text")
        .attr("x", d => x(d.target) + x.bandwidth() / 2)
        .attr("y", d => y(d.source) + y.bandwidth() / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", "middle")
        .style("font-size", x.bandwidth() > 45 ? "11px" : "9px")
        .style("font-weight", "600")
        .style("pointer-events", "none")
        .style("fill", d => Math.abs(d.r) > 0.4 ? "#ffffff" : "var(--ink)")
        .text(d => d.r.toFixed(2));
    }
  }
}
