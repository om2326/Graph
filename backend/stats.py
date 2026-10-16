import numpy as np
import pandas as pd
from scipy import stats
from typing import List, Dict, Any, Optional

def compute_correlations(
    records: List[Dict[str, Any]], 
    columns: List[str], 
    method: str = "pearson",
    min_threshold: float = 0.0,
    max_p_value: float = 1.0
) -> Dict[str, Any]:
    if not records or not columns:
        return {"nodes": [], "links": [], "matrix": [], "columns": [], "stats": {}}
    
    df = pd.DataFrame(records)[columns].apply(pd.to_numeric, errors='coerce').dropna()
    
    if len(df) < 3:
        return {"nodes": [], "links": [], "matrix": [], "columns": [], "stats": {}}
    
    n_cols = len(columns)
    corr_matrix = []
    links = []
    
    # Precompute column summary stats
    col_stats = {}
    for col in columns:
        s = df[col]
        col_stats[col] = {
            "mean": round(float(s.mean()), 2),
            "std": round(float(s.std()), 2),
            "min": round(float(s.min()), 2),
            "max": round(float(s.max()), 2)
        }

    corr_func = stats.pearsonr if method == "pearson" else stats.spearmanr

    for i in range(n_cols):
        row_vals = []
        col_i = columns[i]
        for j in range(n_cols):
            col_j = columns[j]
            if i == j:
                r_val = 1.0
                p_val = 0.0
            else:
                try:
                    res = corr_func(df[col_i], df[col_j])
                    r_val = float(res.statistic) if hasattr(res, 'statistic') else float(res[0])
                    p_val = float(res.pvalue) if hasattr(res, 'pvalue') else float(res[1])
                except Exception:
                    r_val = 0.0
                    p_val = 1.0
                
                if np.isnan(r_val):
                    r_val = 0.0
                if np.isnan(p_val):
                    p_val = 1.0

            row_vals.append({
                "source": col_i,
                "target": col_j,
                "r": round(r_val, 3),
                "p": round(p_val, 4)
            })

            # For undirected graph links, only include upper triangle
            if j > i:
                abs_r = abs(r_val)
                if abs_r >= min_threshold and p_val <= max_p_value:
                    links.append({
                        "source": col_i,
                        "target": col_j,
                        "value": round(r_val, 3),
                        "abs_value": round(abs_r, 3),
                        "p_value": round(p_val, 4),
                        "significant": p_val < 0.05
                    })

        corr_matrix.append(row_vals)

    # Calculate degree strength for each node from the active filtered links
    degree_map = {col: 0.0 for col in columns}
    connection_count = {col: 0 for col in columns}
    for l in links:
        degree_map[l["source"]] += l["abs_value"]
        degree_map[l["target"]] += l["abs_value"]
        connection_count[l["source"]] += 1
        connection_count[l["target"]] += 1

    nodes = []
    for col in columns:
        nodes.append({
            "id": col,
            "name": col,
            "mean": col_stats[col]["mean"],
            "std": col_stats[col]["std"],
            "min": col_stats[col]["min"],
            "max": col_stats[col]["max"],
            "degree_strength": round(degree_map[col], 3),
            "edge_count": connection_count[col]
        })

    # Summary statistics
    strongest_pair = None
    if links:
        sorted_links = sorted(links, key=lambda x: x["abs_value"], reverse=True)
        strongest = sorted_links[0]
        strongest_pair = {
            "source": strongest["source"],
            "target": strongest["target"],
            "value": strongest["value"]
        }

    positive_edges = sum(1 for l in links if l["value"] > 0)
    negative_edges = sum(1 for l in links if l["value"] < 0)

    return {
        "nodes": nodes,
        "links": links,
        "matrix": corr_matrix,
        "columns": columns,
        "sample_size": len(df),
        "stats": {
            "node_count": len(nodes),
            "edge_count": len(links),
            "positive_edges": positive_edges,
            "negative_edges": negative_edges,
            "strongest_pair": strongest_pair
        }
    }

def get_scatter_data(records: List[Dict[str, Any]], x_col: str, y_col: str) -> Dict[str, Any]:
    df = pd.DataFrame(records)[[x_col, y_col]].apply(pd.to_numeric, errors='coerce').dropna()
    if len(df) < 2:
        return {"points": [], "regression": None, "r": 0, "p": 1}

    x_vals = df[x_col].values
    y_vals = df[y_col].values

    slope, intercept, r_val, p_val, std_err = stats.linregress(x_vals, y_vals)

    min_x, max_x = float(np.min(x_vals)), float(np.max(x_vals))
    line_start = {"x": min_x, "y": round(float(slope * min_x + intercept), 2)}
    line_end = {"x": max_x, "y": round(float(slope * max_x + intercept), 2)}

    points = [
        {"x": round(float(r[x_col]), 2), "y": round(float(r[y_col]), 2)}
        for _, r in df.iterrows()
    ]

    return {
        "x_label": x_col,
        "y_label": y_col,
        "points": points,
        "regression": {
            "slope": round(float(slope), 3),
            "intercept": round(float(intercept), 3),
            "r_squared": round(float(r_val**2), 3),
            "r": round(float(r_val), 3),
            "p_value": round(float(p_val), 4),
            "line": [line_start, line_end]
        }
    }

def get_column_distribution(records: List[Dict[str, Any]], col: str, num_bins: int = 10) -> Dict[str, Any]:
    df = pd.DataFrame(records)[[col]].apply(pd.to_numeric, errors='coerce').dropna()
    vals = df[col].values
    if len(vals) == 0:
        return {"col": col, "summary": {}, "histogram": []}

    counts, bin_edges = np.histogram(vals, bins=num_bins)
    histogram = []
    for i in range(len(counts)):
        histogram.append({
            "bin_start": round(float(bin_edges[i]), 1),
            "bin_end": round(float(bin_edges[i+1]), 1),
            "count": int(counts[i])
        })

    summary = {
        "count": len(vals),
        "mean": round(float(np.mean(vals)), 2),
        "std": round(float(np.std(vals, ddof=1)), 2),
        "min": round(float(np.min(vals)), 2),
        "max": round(float(np.max(vals)), 2),
        "q25": round(float(np.percentile(vals, 25)), 2),
        "median": round(float(np.median(vals)), 2),
        "q75": round(float(np.percentile(vals, 75)), 2)
    }

    return {
        "col": col,
        "summary": summary,
        "histogram": histogram
    }
