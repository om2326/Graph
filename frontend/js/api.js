// Frontend API client for Correlation Network Studio

const API_BASE = "/api";

export const api = {
  async getDatasets() {
    const res = await fetch(`${API_BASE}/datasets`);
    if (!res.ok) throw new Error("Failed to fetch datasets");
    return res.json();
  },

  async getCorrelations(datasetId, params = {}) {
    const query = new URLSearchParams();
    if (params.method) query.set("method", params.method);
    if (params.minThreshold !== undefined) query.set("min_threshold", params.minThreshold);
    if (params.maxPValue !== undefined) query.set("max_p_value", params.maxPValue);

    const res = await fetch(`${API_BASE}/datasets/${encodeURIComponent(datasetId)}/correlations?${query.toString()}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to fetch correlations" }));
      throw new Error(err.detail || "Error loading graph");
    }
    return res.json();
  },

  async getScatter(datasetId, x, y) {
    const query = new URLSearchParams({ x, y });
    const res = await fetch(`${API_BASE}/datasets/${encodeURIComponent(datasetId)}/scatter?${query.toString()}`);
    if (!res.ok) throw new Error("Failed to load scatter data");
    return res.json();
  },

  async getDistribution(datasetId, column) {
    const query = new URLSearchParams({ column, bins: 12 });
    const res = await fetch(`${API_BASE}/datasets/${encodeURIComponent(datasetId)}/distribution?${query.toString()}`);
    if (!res.ok) throw new Error("Failed to load distribution data");
    return res.json();
  },

  async uploadCSV(formData) {
    const res = await fetch(`${API_BASE}/datasets/upload`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Upload failed" }));
      throw new Error(err.detail || "Upload failed");
    }
    return res.json();
  },

  async deleteDataset(datasetId) {
    const res = await fetch(`${API_BASE}/datasets/${encodeURIComponent(datasetId)}`, {
      method: "DELETE",
    });
    if (!res.ok) throw new Error("Failed to delete dataset");
    return res.json();
  }
};
