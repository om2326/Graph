import { api } from "./api.js";
import { NetworkGraph } from "./graph.js";
import { CorrelationHeatmap } from "./heatmap.js";
import { renderScatterPlot, renderHistogram } from "./charts.js";

class App {
  constructor() {
    this.state = {
      datasetId: "student-performance",
      method: "pearson",
      threshold: 0.35,
      onlySignificant: false,
      activeView: "graph",
      graphData: null,
      datasets: []
    };

    this.init();
  }

  async init() {
    this.graph = new NetworkGraph("#graph-canvas-container", "#main-tooltip", {
      onEdgeClick: (s, t) => this.openScatterModal(s, t),
      onNodeClick: (node, links) => this.handleNodeClick(node, links)
    });

    this.heatmap = new CorrelationHeatmap("#heatmap-canvas-container", "#main-tooltip", {
      onCellClick: (s, t) => this.openScatterModal(s, t)
    });

    this.bindEvents();
    await this.loadDatasetsList();
    await this.refreshAnalysis();
  }

  bindEvents() {
    // Dataset selector
    const datasetSelect = document.getElementById("dataset-select");
    datasetSelect.addEventListener("change", (e) => {
      this.state.datasetId = e.target.value;
      this.refreshAnalysis();
    });

    // Correlation Method
    document.querySelectorAll("input[name='corr-method']").forEach(radio => {
      radio.addEventListener("change", (e) => {
        this.state.method = e.target.value;
        this.refreshAnalysis();
      });
    });

    // Threshold Slider
    const threshInput = document.getElementById("threshold-range");
    const threshDisplay = document.getElementById("threshold-val");
    threshInput.addEventListener("input", (e) => {
      const val = parseFloat(e.target.value);
      threshDisplay.textContent = val.toFixed(2);
      this.state.threshold = val;
      this.refreshAnalysis();
    });

    // Significance filter checkbox
    const sigCheck = document.getElementById("sig-filter-check");
    sigCheck.addEventListener("change", (e) => {
      this.state.onlySignificant = e.target.checked;
      this.refreshAnalysis();
    });

    // View toggle buttons (Graph vs Heatmap)
    const btnGraph = document.getElementById("btn-view-graph");
    const btnHeatmap = document.getElementById("btn-view-heatmap");
    const graphViewEl = document.getElementById("graph-view");
    const heatmapViewEl = document.getElementById("heatmap-view");

    btnGraph.addEventListener("click", () => {
      this.state.activeView = "graph";
      btnGraph.classList.add("active");
      btnHeatmap.classList.remove("active");
      graphViewEl.style.display = "block";
      heatmapViewEl.style.display = "none";
      this.graph.resize();
    });

    btnHeatmap.addEventListener("click", () => {
      this.state.activeView = "heatmap";
      btnHeatmap.classList.add("active");
      btnGraph.classList.remove("active");
      graphViewEl.style.display = "none";
      heatmapViewEl.style.display = "block";
      if (this.state.graphData) {
        this.heatmap.update(this.state.graphData.matrix, this.state.graphData.columns);
      }
    });

    // Zoom buttons
    document.getElementById("btn-zoom-in").addEventListener("click", () => this.graph.zoomIn());
    document.getElementById("btn-zoom-out").addEventListener("click", () => this.graph.zoomOut());
    document.getElementById("btn-zoom-reset").addEventListener("click", () => this.graph.resetZoom());

    // Export SVG
    document.getElementById("btn-export-svg").addEventListener("click", () => this.graph.exportSVG());

    // Modal controls for CSV Upload
    const uploadModal = document.getElementById("upload-modal");
    const btnOpenUpload = document.getElementById("btn-open-upload");
    const btnCloseUpload = document.getElementById("btn-close-upload");
    const uploadForm = document.getElementById("upload-form");

    btnOpenUpload.addEventListener("click", () => uploadModal.classList.add("active"));
    btnCloseUpload.addEventListener("click", () => uploadModal.classList.remove("active"));
    uploadModal.addEventListener("click", (e) => {
      if (e.target === uploadModal) uploadModal.classList.remove("active");
    });

    uploadForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fileInput = document.getElementById("upload-file");
      const nameInput = document.getElementById("upload-name");
      const descInput = document.getElementById("upload-desc");

      if (!fileInput.files || fileInput.files.length === 0) {
        alert("Please select a CSV file.");
        return;
      }

      const formData = new FormData();
      formData.append("file", fileInput.files[0]);
      formData.append("name", nameInput.value || fileInput.files[0].name);
      formData.append("description", descInput.value || "");

      try {
        const newDs = await api.uploadCSV(formData);
        uploadModal.classList.remove("active");
        uploadForm.reset();
        await this.loadDatasetsList();
        this.state.datasetId = newDs.id;
        document.getElementById("dataset-select").value = newDs.id;
        await this.refreshAnalysis();
      } catch (err) {
        alert("Upload error: " + err.message);
      }
    });

    // Scatter modal controls
    const scatterModal = document.getElementById("scatter-modal");
    const btnCloseScatter = document.getElementById("btn-close-scatter");
    btnCloseScatter.addEventListener("click", () => scatterModal.classList.remove("active"));
    scatterModal.addEventListener("click", (e) => {
      if (e.target === scatterModal) scatterModal.classList.remove("active");
    });
  }

  async loadDatasetsList() {
    try {
      const datasets = await api.getDatasets();
      this.state.datasets = datasets;
      const select = document.getElementById("dataset-select");
      select.innerHTML = "";
      datasets.forEach(ds => {
        const opt = document.createElement("option");
        opt.value = ds.id;
        opt.textContent = `${ds.name} (${ds.row_count} rows, ${ds.columns.length} vars)`;
        select.appendChild(opt);
      });
      select.value = this.state.datasetId;
    } catch (err) {
      console.error("Failed to load dataset list:", err);
    }
  }

  async refreshAnalysis() {
    try {
      const data = await api.getCorrelations(this.state.datasetId, {
        method: this.state.method,
        minThreshold: this.state.threshold,
        maxPValue: this.state.onlySignificant ? 0.05 : 1.0
      });

      this.state.graphData = data;
      this.updateSidebarStats(data);

      if (this.state.activeView === "graph") {
        this.graph.update(data);
      } else {
        this.heatmap.update(data.matrix, data.columns);
      }
    } catch (err) {
      console.error("Analysis update failed:", err);
    }
  }

  updateSidebarStats(data) {
    document.getElementById("stat-sample").textContent = data.sample_size || "–";
    document.getElementById("stat-nodes").textContent = data.stats.node_count || "–";
    document.getElementById("stat-edges").textContent = data.stats.edge_count || 0;
    document.getElementById("stat-pos-neg").textContent = `${data.stats.positive_edges} / ${data.stats.negative_edges}`;

    const strongEl = document.getElementById("stat-strong");
    if (data.stats.strongest_pair) {
      const sp = data.stats.strongest_pair;
      strongEl.textContent = `${sp.source} – ${sp.target} (${sp.value > 0 ? '+' : ''}${sp.value})`;
    } else {
      strongEl.textContent = "None";
    }

    // Dataset info
    if (data.dataset) {
      document.getElementById("dataset-desc").textContent = data.dataset.description || "";
    }
  }

  async handleNodeClick(node, connectedLinks) {
    const inspector = document.getElementById("inspector-box");
    if (!node || !connectedLinks) {
      inspector.innerHTML = `<div style="color:var(--muted);">Click any node or link to inspect statistics and distributions.</div>`;
      return;
    }

    inspector.innerHTML = `
      <h3>${node.name}</h3>
      <div style="font-size:12px;color:var(--muted);margin-bottom:8px;">
        Mean: <b>${node.mean}</b> | Std: <b>${node.std}</b> | Active Links: <b>${connectedLinks.length}</b>
      </div>
      <div id="inspector-histogram" style="margin-top:6px;"></div>
      <div style="margin-top:8px;font-size:12px;">
        <strong>Correlations:</strong>
        <ul style="padding-left:16px;margin:4px 0 0 0;">
          ${connectedLinks.map(l => {
            const other = (l.source.id || l.source) === node.id ? (l.target.id || l.target) : (l.source.id || l.source);
            return `<li>${other}: <b>${l.value > 0 ? '+' : ''}${l.value}</b> (p=${l.p_value})</li>`;
          }).join("")}
        </ul>
      </div>
    `;

    // Fetch and render distribution histogram
    try {
      const dist = await api.getDistribution(this.state.datasetId, node.name);
      renderHistogram("#inspector-histogram", dist);
    } catch (err) {
      console.error(err);
    }
  }

  async openScatterModal(source, target) {
    const modal = document.getElementById("scatter-modal");
    document.getElementById("scatter-title").textContent = `Relationship: ${source} vs ${target}`;
    modal.classList.add("active");

    const container = document.getElementById("scatter-chart-container");
    container.innerHTML = `<div style="padding:40px;text-align:center;color:var(--muted);">Loading scatter plot...</div>`;

    try {
      const data = await api.getScatter(this.state.datasetId, source, target);
      renderScatterPlot("#scatter-chart-container", data);

      if (data.regression) {
        document.getElementById("scatter-stats").innerHTML = `
          <strong>Pearson r:</strong> ${data.regression.r} &nbsp;|&nbsp;
          <strong>R²:</strong> ${data.regression.r_squared} &nbsp;|&nbsp;
          <strong>Equation:</strong> y = ${data.regression.slope}x + ${data.regression.intercept} &nbsp;|&nbsp;
          <strong>p-value:</strong> ${data.regression.p_value}
        `;
      }
    } catch (err) {
      container.innerHTML = `<div style="color:red;padding:20px;">Error loading scatter plot: ${err.message}</div>`;
    }
  }
}

// Instantiate application on DOM load
window.addEventListener("DOMContentLoaded", () => {
  window.app = new App();
});
