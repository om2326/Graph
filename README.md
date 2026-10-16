# Correlation Network Studio (Full-Stack)

An interactive, full-stack visual analytics platform for exploring statistical correlations, dependencies, and relationships across numeric datasets using force-directed network graphs, correlation heatmaps, and regression scatter plots.

---

## Architecture Overview

```
graph_visualization/
├── backend/
│   ├── app.py              # FastAPI application, REST endpoints, and static file serving
│   ├── database.py         # SQLite database schema, connections, and CRUD operations
│   ├── stats.py            # Statistical computation (Pearson/Spearman, p-values, regression, histograms)
│   └── seed_data.py        # Seed datasets (Student Performance, Macroeconomic Indicators)
├── frontend/
│   ├── index.html          # Modern dashboard application layout
│   ├── css/
│   │   └── styles.css      # Polished, responsive stylesheet
│   └── js/
│       ├── api.js          # Client-side API service
│       ├── graph.js        # D3.js Force-Directed Graph with Zoom, Pan, Drag, Pinning
│       ├── heatmap.js      # D3.js Correlation Heatmap Matrix
│       ├── charts.js       # Scatter Plot with Linear Regression & Distribution Histograms
│       └── app.js          # App controller & state management
├── data/
│   └── app.db              # SQLite database (auto-created on launch)
├── run.py                  # Single-command launcher script
├── requirements.txt        # Backend dependencies
└── correlation_network.html# Original single-file prototype (preserved)
```

---

## Features

### 1. Frontend (Interactive Dashboard)
* **D3.js Force-Directed Network Graph**:
  * Nodes sized by degree connection strength.
  * Positive correlations rendered in **teal (solid lines)**; negative correlations in **rust (dashed lines)**.
  * Edge thickness scales with correlation magnitude $|r|$.
  * **Interactive Zoom & Pan** (`d3.zoom`) with dedicated zoom buttons and reset view.
  * **Drag & Double-Click Pinning**: Drag nodes freely or double-click to lock/unlock them in place.
  * **Hover Tooltips**: Live inspection of $r$-values, $p$-values, and statistical significance.
* **Correlation Heatmap Matrix**:
  * Toggle between Network Graph view and full symmetric $N \times N$ correlation grid.
  * Diverging color palette from negative (dark rust) through neutral to positive (deep teal).
* **Linked Scatter Plot Modal**:
  * Clicking any edge or heatmap cell opens an interactive 2D scatter plot showing all observations.
  * Automatically calculates and overlays the **linear regression trendline**, $R^2$, slope, and exact $p$-value.
* **Inspector & Distribution Histograms**:
  * Clicking any node highlights its neighbors, dims unrelated elements, and opens a score frequency histogram with mean, standard deviation, and quartile statistics.
* **Custom CSV Uploader**:
  * Drag-and-drop or select any custom CSV file.
  * The backend automatically identifies numeric variables, validates rows, saves the dataset into the database, and renders the graph.
* **SVG Vector Export**:
  * One-click export of the network graph as a scalable vector graphic (`.svg`).

### 2. Backend (FastAPI + SciPy + Pandas)
* Built with Python's high-performance **FastAPI** framework.
* Computes correlations via **SciPy**:
  * Supports both **Pearson** ($r$) and **Spearman Rank** ($\rho$) correlation methods.
  * Calculates two-tailed $p$-values for every variable pair.
  * Linear regression via `scipy.stats.linregress`.
  * Histogram binning via `numpy.histogram`.

### 3. Database (SQLite)
* Zero-configuration, file-based **SQLite** storage (`data/app.db`).
* Persists datasets, variable metadata, and raw rows.
* Comes pre-seeded with:
  1. **Student Academic Performance**: 100 students across 8 subjects showing latent quantitative, verbal, and memory clusters.
  2. **Macroeconomic Indicators**: 80 periods across GDP, Inflation, Unemployment, Interest Rates, Consumer Confidence, and Stock Index showing both direct and inverse relationships.

---

## Quick Start

### 1. Requirements
Ensure Python is available. The required packages are listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Run the Application
Launch the server with the included runner script:
```bash
python run.py
```

### 3. Access the Studio
* **Frontend Web App**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive API Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/datasets` | List all available datasets |
| `GET` | `/api/datasets/{id}` | Retrieve metadata for a specific dataset |
| `POST` | `/api/datasets/upload` | Upload and ingest a custom CSV dataset |
| `DELETE`| `/api/datasets/{id}` | Delete a custom uploaded dataset |
| `GET` | `/api/datasets/{id}/correlations` | Compute correlation matrix, active edges, nodes, and stats |
| `GET` | `/api/datasets/{id}/scatter?x=...&y=...` | Retrieve points and linear regression for two variables |
| `GET` | `/api/datasets/{id}/distribution?column=...` | Get frequency histogram and descriptive statistics |

---

## Project Presentation Deck

The project includes an executive and technical presentation deck covering the end-to-end system architecture, statistical foundations, and D3 physics mechanics:

* **PowerPoint Presentation**: [`presentation.pptx`](file:///c:/Users/lenovo/Desktop/graph_visualization/presentation.pptx) or [`Correlation_Network_Studio_Presentation.pptx`](file:///c:/Users/lenovo/Desktop/graph_visualization/Correlation_Network_Studio_Presentation.pptx) (16:9 widescreen, 12 slides, custom layouts & high-DPI assets)
* **PDF Export**: [`presentation.pdf`](file:///c:/Users/lenovo/Desktop/graph_visualization/presentation.pdf) or [`Correlation_Network_Studio_Presentation.pdf`](file:///c:/Users/lenovo/Desktop/graph_visualization/Correlation_Network_Studio_Presentation.pdf)
* **Web-Based Presentation**: Open [`presentation.html`](file:///c:/Users/lenovo/Desktop/graph_visualization/presentation.html) in any browser, or visit `http://127.0.0.1:8000/presentation` when running the server
* **Regenerate Deck & Assets**:
  ```bash
  python generate_deck_assets.py
  python build_studio_presentation.py
  powershell -File export_pdf.ps1
  ```

