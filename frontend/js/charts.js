// Sub-charts: Interactive Scatter Plot with Regression & Distribution Histogram

export function renderScatterPlot(containerSelector, data) {
  const container = d3.select(containerSelector);
  container.selectAll("*").remove();

  if (!data || !data.points || data.points.length === 0) {
    container.append("p").text("No scatter data available.");
    return;
  }

  const margin = { top: 20, right: 30, bottom: 45, left: 55 };
  const width = 520 - margin.left - margin.right;
  const height = 340 - margin.top - margin.bottom;

  const svg = container.append("svg")
    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    .style("width", "100%")
    .style("height", "auto");

  const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

  const xVals = data.points.map(d => d.x);
  const yVals = data.points.map(d => d.y);

  const xExtent = d3.extent(xVals);
  const yExtent = d3.extent(yVals);

  const xPad = (xExtent[1] - xExtent[0]) * 0.08 || 1;
  const yPad = (yExtent[1] - yExtent[0]) * 0.08 || 1;

  const x = d3.scaleLinear()
    .domain([xExtent[0] - xPad, xExtent[1] + xPad])
    .range([0, width]);

  const y = d3.scaleLinear()
    .domain([yExtent[0] - yPad, yExtent[1] + yPad])
    .range([height, 0]);

  // Grid lines
  g.append("g")
    .attr("class", "grid")
    .attr("stroke", "#e5e7eb")
    .attr("stroke-dasharray", "2,2")
    .call(d3.axisLeft(y).tickSize(-width).tickFormat(""));

  // Axes
  g.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x));

  g.append("g").call(d3.axisLeft(y));

  // Axis Labels
  g.append("text")
    .attr("text-anchor", "middle")
    .attr("x", width / 2)
    .attr("y", height + 38)
    .style("font-size", "12px")
    .style("font-weight", "600")
    .text(data.x_label);

  g.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", -38)
    .style("font-size", "12px")
    .style("font-weight", "600")
    .text(data.y_label);

  // Scatter dots
  g.selectAll(".dot")
    .data(data.points)
    .enter()
    .append("circle")
    .attr("cx", d => x(d.x))
    .attr("cy", d => y(d.y))
    .attr("r", 4.5)
    .attr("fill", "#2563eb")
    .attr("opacity", 0.75)
    .attr("stroke", "#fff")
    .attr("stroke-width", 1);

  // Linear Regression line
  if (data.regression && data.regression.line) {
    const lineData = data.regression.line;
    g.append("line")
      .attr("x1", x(lineData[0].x))
      .attr("y1", y(lineData[0].y))
      .attr("x2", x(lineData[1].x))
      .attr("y2", y(lineData[1].y))
      .attr("stroke", "#b5452d")
      .attr("stroke-width", 2.5);
  }
}

export function renderHistogram(containerSelector, data) {
  const container = d3.select(containerSelector);
  container.selectAll("*").remove();

  if (!data || !data.histogram || data.histogram.length === 0) {
    container.append("p").text("No distribution data available.");
    return;
  }

  const margin = { top: 15, right: 15, bottom: 35, left: 35 };
  const width = 280 - margin.left - margin.right;
  const height = 150 - margin.top - margin.bottom;

  const svg = container.append("svg")
    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    .style("width", "100%")
    .style("height", "auto");

  const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

  const x = d3.scaleBand()
    .domain(data.histogram.map(d => `${d.bin_start}`))
    .range([0, width])
    .padding(0.15);

  const maxCount = d3.max(data.histogram, d => d.count) || 1;
  const y = d3.scaleLinear().domain([0, maxCount]).range([height, 0]);

  // Bars
  g.selectAll(".bar")
    .data(data.histogram)
    .enter()
    .append("rect")
    .attr("x", d => x(`${d.bin_start}`))
    .attr("y", d => y(d.count))
    .attr("width", x.bandwidth())
    .attr("height", d => height - y(d.count))
    .attr("fill", "var(--accent-pos)")
    .attr("rx", 2);

  // X Axis
  g.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).tickValues(x.domain().filter((_, i) => i % 2 === 0)))
    .selectAll("text")
    .style("font-size", "9px");

  // Y Axis
  g.append("g")
    .call(d3.axisLeft(y).ticks(4))
    .selectAll("text")
    .style("font-size", "9px");
}
