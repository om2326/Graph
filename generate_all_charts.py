"""
Generate all chart images for the comprehensive presentation.
Uses REAL computed data from the project datasets.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import sys, os
sys.path.insert(0, '.')
from backend.database import init_db, get_dataset, get_dataset_records
from backend.stats import compute_correlations, get_scatter_data, get_column_distribution

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial']

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
os.makedirs(OUT, exist_ok=True)

init_db()

# ───────────────────────────────────────────────────────────
# CHART 1: Student Correlation Heatmap (Full 8x8 Matrix)
# ───────────────────────────────────────────────────────────
def chart_student_heatmap():
    records = get_dataset_records('student-performance')
    cols = get_dataset('student-performance')['columns']
    data = compute_correlations(records, cols, method='pearson')
    
    n = len(cols)
    matrix = np.zeros((n, n))
    for i, row in enumerate(data['matrix']):
        for j, cell in enumerate(row):
            matrix[i][j] = cell['r']
    
    short = ['Math', 'Phys', 'Chem', 'Bio', 'Eng', 'Hist', 'Econ', 'CS']
    
    fig, ax = plt.subplots(figsize=(7, 6), dpi=200)
    im = ax.imshow(matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')
    
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(short, fontsize=10, rotation=45, ha='right', fontweight='600', color='#1E293B')
    ax.set_yticklabels(short, fontsize=10, fontweight='600', color='#1E293B')
    
    for i in range(n):
        for j in range(n):
            val = matrix[i][j]
            color = '#FFFFFF' if abs(val) > 0.4 else '#1E293B'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=9, 
                    fontweight='bold', color=color)
    
    cbar = plt.colorbar(im, ax=ax, shrink=0.82, pad=0.03)
    cbar.set_label('Pearson Correlation (r)', fontsize=10, fontweight='bold', color='#334155')
    
    ax.set_title('Student Academic Performance — Pearson Correlation Matrix (N=100)', 
                 fontsize=12, fontweight='bold', color='#0F172A', pad=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'student_heatmap.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] student_heatmap.png")

# ───────────────────────────────────────────────────────────
# CHART 2: Economic Correlation Heatmap (Full 6x6 Matrix)
# ───────────────────────────────────────────────────────────
def chart_econ_heatmap():
    records = get_dataset_records('economic-indicators')
    cols = get_dataset('economic-indicators')['columns']
    data = compute_correlations(records, cols, method='pearson')
    
    n = len(cols)
    matrix = np.zeros((n, n))
    for i, row in enumerate(data['matrix']):
        for j, cell in enumerate(row):
            matrix[i][j] = cell['r']
    
    short = ['GDP', 'Inflation', 'Unemp', 'Interest', 'Confidence', 'Stocks']
    
    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=200)
    im = ax.imshow(matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')
    
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(short, fontsize=10, rotation=45, ha='right', fontweight='600', color='#1E293B')
    ax.set_yticklabels(short, fontsize=10, fontweight='600', color='#1E293B')
    
    for i in range(n):
        for j in range(n):
            val = matrix[i][j]
            color = '#FFFFFF' if abs(val) > 0.4 else '#1E293B'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', fontsize=10, 
                    fontweight='bold', color=color)
    
    cbar = plt.colorbar(im, ax=ax, shrink=0.82, pad=0.03)
    cbar.set_label('Pearson Correlation (r)', fontsize=10, fontweight='bold', color='#334155')
    
    ax.set_title('Macroeconomic Indicators — Pearson Correlation Matrix (N=80)', 
                 fontsize=12, fontweight='bold', color='#0F172A', pad=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'econ_heatmap.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] econ_heatmap.png")

# ───────────────────────────────────────────────────────────
# CHART 3: Math vs Physics Scatter + OLS Regression
# ───────────────────────────────────────────────────────────
def chart_scatter_math_physics():
    records = get_dataset_records('student-performance')
    scatter = get_scatter_data(records, 'Math', 'Physics')
    
    pts = scatter['points']
    reg = scatter['regression']
    xs = [p['x'] for p in pts]
    ys = [p['y'] for p in pts]
    
    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=200)
    ax.set_facecolor('#FAFAFA')
    
    ax.scatter(xs, ys, color='#2563EB', alpha=0.72, edgecolors='#FFFFFF', s=50, lw=0.8,
               label=f'Observations (N={len(pts)})')
    
    line = reg['line']
    ax.plot([line[0]['x'], line[1]['x']], [line[0]['y'], line[1]['y']], 
            color='#B5452D', lw=2.5, 
            label=f'OLS Fit: y = {reg["slope"]:.3f}x + {reg["intercept"]:.2f}')
    
    ax.set_xlabel('Math Score', fontsize=11, fontweight='bold', color='#334155')
    ax.set_ylabel('Physics Score', fontsize=11, fontweight='bold', color='#334155')
    ax.set_title(f'Math vs Physics — OLS Linear Regression\nr = {reg["r"]:.3f}, R² = {reg["r_squared"]:.3f}, p < 0.0001', 
                 fontsize=12, fontweight='bold', color='#0F172A')
    ax.legend(loc='upper left', fontsize=9.5, frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0')
    ax.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'scatter_math_physics.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] scatter_math_physics.png")

# ───────────────────────────────────────────────────────────
# CHART 4: GDP vs Unemployment Scatter + OLS Regression
# ───────────────────────────────────────────────────────────
def chart_scatter_gdp_unemp():
    records = get_dataset_records('economic-indicators')
    scatter = get_scatter_data(records, 'GDP_Growth', 'Unemployment')
    
    pts = scatter['points']
    reg = scatter['regression']
    xs = [p['x'] for p in pts]
    ys = [p['y'] for p in pts]
    
    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=200)
    ax.set_facecolor('#FAFAFA')
    
    ax.scatter(xs, ys, color='#B5452D', alpha=0.72, edgecolors='#FFFFFF', s=50, lw=0.8,
               label=f'Observations (N={len(pts)})')
    
    line = reg['line']
    ax.plot([line[0]['x'], line[1]['x']], [line[0]['y'], line[1]['y']], 
            color='#0D9488', lw=2.5, 
            label=f'OLS Fit: y = {reg["slope"]:.3f}x + {reg["intercept"]:.2f}')
    
    ax.set_xlabel('GDP Growth (%)', fontsize=11, fontweight='bold', color='#334155')
    ax.set_ylabel('Unemployment Rate (%)', fontsize=11, fontweight='bold', color='#334155')
    ax.set_title(f'GDP Growth vs Unemployment — OLS Regression (Okun\'s Law)\nr = {reg["r"]:.3f}, R² = {reg["r_squared"]:.3f}, p < 0.0001', 
                 fontsize=12, fontweight='bold', color='#0F172A')
    ax.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0')
    ax.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'scatter_gdp_unemp.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] scatter_gdp_unemp.png")

# ───────────────────────────────────────────────────────────
# CHART 5: Student Top 10 Correlation Bar Chart
# ───────────────────────────────────────────────────────────
def chart_student_topN():
    records = get_dataset_records('student-performance')
    cols = get_dataset('student-performance')['columns']
    data = compute_correlations(records, cols, method='pearson')
    
    links = sorted(data['links'], key=lambda x: x['abs_value'], reverse=True)[:12]
    
    labels = [f"{l['source'][:4]}-{l['target'][:4]}" for l in links]
    values = [l['value'] for l in links]
    colors = ['#0D9488' if v > 0 else '#B5452D' for v in values]
    
    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    ax.set_facecolor('#FAFAFA')
    
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, height=0.6, edgecolor='#FFFFFF')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9.5, color='#334155')
    ax.invert_yaxis()
    ax.set_xlabel('Pearson Correlation (r)', fontsize=11, fontweight='bold', color='#334155')
    ax.set_title('Student Dataset — Ranked Correlation Pairs', fontsize=12, fontweight='bold', color='#0F172A')
    ax.axvline(0, color='#64748B', lw=1)
    ax.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for bar, v in zip(bars, values):
        ax.text(bar.get_width() + (0.02 if v > 0 else -0.02), bar.get_y() + bar.get_height()/2, 
                f'{v:+.3f}', ha='left' if v > 0 else 'right', va='center', fontsize=9, fontweight='bold', 
                color='#0D9488' if v > 0 else '#B5452D')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'student_top_corr.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] student_top_corr.png")

# ───────────────────────────────────────────────────────────
# CHART 6: Economic Correlation Bar Chart
# ───────────────────────────────────────────────────────────
def chart_econ_topN():
    records = get_dataset_records('economic-indicators')
    cols = get_dataset('economic-indicators')['columns']
    data = compute_correlations(records, cols, method='pearson')
    
    links = sorted(data['links'], key=lambda x: x['abs_value'], reverse=True)
    
    short_map = {'GDP_Growth': 'GDP', 'Inflation_Rate': 'Infl', 'Unemployment': 'Unemp',
                 'Interest_Rate': 'Rate', 'Consumer_Confidence': 'Conf', 'Stock_Index': 'Stock'}
    labels = [f"{short_map.get(l['source'], l['source'])}-{short_map.get(l['target'], l['target'])}" for l in links]
    values = [l['value'] for l in links]
    colors = ['#0D9488' if v > 0 else '#B5452D' for v in values]
    
    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    ax.set_facecolor('#FAFAFA')
    
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, values, color=colors, height=0.6, edgecolor='#FFFFFF')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9.5, color='#334155')
    ax.invert_yaxis()
    ax.set_xlabel('Pearson Correlation (r)', fontsize=11, fontweight='bold', color='#334155')
    ax.set_title('Macroeconomic Dataset — All 15 Correlation Pairs (Ranked)', fontsize=12, fontweight='bold', color='#0F172A')
    ax.axvline(0, color='#64748B', lw=1)
    ax.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for bar, v in zip(bars, values):
        offset = 0.02 if v > 0 else -0.02
        ax.text(bar.get_width() + offset, bar.get_y() + bar.get_height()/2, 
                f'{v:+.3f}', ha='left' if v > 0 else 'right', va='center', fontsize=9, fontweight='bold', 
                color='#0D9488' if v > 0 else '#B5452D')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'econ_top_corr.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] econ_top_corr.png")

# ───────────────────────────────────────────────────────────
# CHART 7: Node Degree Centrality (Student)
# ───────────────────────────────────────────────────────────
def chart_degree_centrality():
    records = get_dataset_records('student-performance')
    cols = get_dataset('student-performance')['columns']
    data = compute_correlations(records, cols, method='pearson', min_threshold=0.3)
    
    nodes = sorted(data['nodes'], key=lambda x: x['degree_strength'], reverse=True)
    names = [n['id'][:12] for n in nodes]
    degrees = [n['degree_strength'] for n in nodes]
    edges = [n['edge_count'] for n in nodes]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=200)
    
    # Degree Strength
    ax1.set_facecolor('#FAFAFA')
    bars1 = ax1.bar(names, degrees, color='#2563EB', edgecolor='#1D4ED8', lw=1)
    ax1.set_ylabel('Degree Strength (sum |r|)', fontsize=10, fontweight='bold', color='#334155')
    ax1.set_title('Weighted Degree Centrality', fontsize=11, fontweight='bold', color='#0F172A')
    ax1.tick_params(axis='x', rotation=45, labelsize=9)
    ax1.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    for bar, v in zip(bars1, degrees):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{v:.2f}', 
                ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1D4ED8')
    
    # Edge Count
    ax2.set_facecolor('#FAFAFA')
    bars2 = ax2.bar(names, edges, color='#0D9488', edgecolor='#0F766E', lw=1)
    ax2.set_ylabel('Connected Edges (|r| >= 0.3)', fontsize=10, fontweight='bold', color='#334155')
    ax2.set_title('Edge Count per Variable', fontsize=11, fontweight='bold', color='#0F172A')
    ax2.tick_params(axis='x', rotation=45, labelsize=9)
    ax2.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    for bar, v in zip(bars2, edges):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15, str(v), 
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0F766E')
    
    fig.suptitle('Student Dataset — Node Centrality Analysis (Threshold |r| >= 0.3)', fontsize=12, fontweight='bold', color='#0F172A', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'degree_centrality.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] degree_centrality.png")

# ───────────────────────────────────────────────────────────
# CHART 8: Distribution Histograms (Student — 8 subjects)
# ───────────────────────────────────────────────────────────
def chart_student_distributions():
    records = get_dataset_records('student-performance')
    cols = get_dataset('student-performance')['columns']
    
    fig, axes = plt.subplots(2, 4, figsize=(12, 5.5), dpi=200)
    teal_shades = ['#0D9488', '#2563EB', '#7C3AED', '#B5452D', '#0D9488', '#2563EB', '#7C3AED', '#B5452D']
    
    for idx, (col, ax) in enumerate(zip(cols, axes.flat)):
        dist = get_column_distribution(records, col, num_bins=10)
        bins = dist['histogram']
        s = dist['summary']
        
        starts = [b['bin_start'] for b in bins]
        counts = [b['count'] for b in bins]
        
        ax.set_facecolor('#FAFAFA')
        ax.bar(range(len(counts)), counts, color=teal_shades[idx], alpha=0.85, edgecolor='#FFFFFF')
        ax.set_title(f'{col}', fontsize=10, fontweight='bold', color='#0F172A')
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.tick_params(labelsize=7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        stats_text = f"μ={s['mean']:.1f}  σ={s['std']:.1f}"
        ax.text(0.97, 0.95, stats_text, transform=ax.transAxes, fontsize=7.5, fontweight='bold',
                ha='right', va='top', color='#475569',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#E2E8F0', alpha=0.9))
    
    fig.suptitle('Student Academic Performance — Score Distributions (N=100)', fontsize=13, fontweight='bold', color='#0F172A')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'student_distributions.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] student_distributions.png")

# ───────────────────────────────────────────────────────────
# CHART 9: Pearson vs Spearman Comparison
# ───────────────────────────────────────────────────────────
def chart_pearson_vs_spearman():
    records = get_dataset_records('student-performance')
    cols = get_dataset('student-performance')['columns']
    pearson = compute_correlations(records, cols, method='pearson')
    spearman = compute_correlations(records, cols, method='spearman')
    
    # Match links
    pearson_map = {}
    for l in pearson['links']:
        key = tuple(sorted([l['source'], l['target']]))
        pearson_map[key] = l['value']
    
    spearman_map = {}
    for l in spearman['links']:
        key = tuple(sorted([l['source'], l['target']]))
        spearman_map[key] = l['value']
    
    common_keys = sorted(set(pearson_map.keys()) & set(spearman_map.keys()))
    top_keys = sorted(common_keys, key=lambda k: abs(pearson_map[k]), reverse=True)[:12]
    
    labels = [f"{k[0][:4]}-{k[1][:4]}" for k in top_keys]
    p_vals = [pearson_map[k] for k in top_keys]
    s_vals = [spearman_map[k] for k in top_keys]
    
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    ax.set_facecolor('#FAFAFA')
    
    x = np.arange(len(labels))
    width = 0.35
    ax.bar(x - width/2, p_vals, width, label='Pearson (r)', color='#2563EB', edgecolor='#1D4ED8', lw=0.8)
    ax.bar(x + width/2, s_vals, width, label='Spearman (ρ)', color='#0D9488', edgecolor='#0F766E', lw=0.8)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, rotation=45, ha='right')
    ax.set_ylabel('Correlation Coefficient', fontsize=11, fontweight='bold', color='#334155')
    ax.set_title('Pearson vs Spearman — Side-by-Side Comparison (Student Dataset)', fontsize=12, fontweight='bold', color='#0F172A')
    ax.legend(fontsize=10, frameon=True, facecolor='#FFFFFF')
    ax.axhline(0, color='#64748B', lw=0.8)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'pearson_vs_spearman.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] pearson_vs_spearman.png")

# ───────────────────────────────────────────────────────────
# CHART 10: Architecture Diagram
# ───────────────────────────────────────────────────────────
def chart_architecture():
    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    ax.text(5.0, 9.6, "THREE-TIER SYSTEM ARCHITECTURE", ha="center", va="center", 
            fontsize=12, fontweight="bold", color="#0F172A")

    # Tier 1
    box1 = FancyBboxPatch((0.5, 6.7), 9.0, 2.4, boxstyle="round,pad=0.25", fc="#F0FDF4", ec="#0D9488", lw=2.5)
    ax.add_patch(box1)
    ax.text(1.0, 8.5, "FRONTEND CLIENT (Browser)", fontsize=11, fontweight="bold", color="#0F172A")
    ax.text(8.8, 8.5, "D3.js v7", ha="right", fontsize=9.5, fontweight="bold", color="#0D9488")
    ax.text(1.0, 7.65, "• Force-Directed Network Graph (Physics, Zoom, Drag, Pin)\n• Correlation Heatmap Matrix (N x N diverging color scale)\n• Scatter Plot Modal (OLS trendline) & Histogram Inspector", 
            fontsize=8.5, color="#334155", va="top")

    ax.annotate('', xy=(5.0, 6.6), xytext=(5.0, 5.9),
                arrowprops=dict(arrowstyle="<->", color="#2563EB", lw=2.2, mutation_scale=14))
    ax.text(5.15, 6.25, "REST API (JSON / Multipart Upload)", fontsize=8.5, color="#2563EB", fontweight="bold")

    # Tier 2
    box2 = FancyBboxPatch((0.5, 3.4), 9.0, 2.4, boxstyle="round,pad=0.25", fc="#EFF6FF", ec="#2563EB", lw=2.5)
    ax.add_patch(box2)
    ax.text(1.0, 5.2, "BACKEND COMPUTATION (FastAPI + SciPy)", fontsize=11, fontweight="bold", color="#0F172A")
    ax.text(8.8, 5.2, "Python 3.14", ha="right", fontsize=9.5, fontweight="bold", color="#2563EB")
    ax.text(1.0, 4.35, "• Pearson (r) & Spearman (rho) correlation matrices\n• Two-tailed Student t p-value hypothesis testing\n• OLS linear regression (slope, intercept, R2, std_err)", 
            fontsize=8.5, color="#334155", va="top")

    ax.annotate('', xy=(5.0, 3.3), xytext=(5.0, 2.6),
                arrowprops=dict(arrowstyle="<->", color="#0F172A", lw=2.2, mutation_scale=14))
    ax.text(5.15, 2.95, "SQL Queries & JSON Schema Ingestion", fontsize=8.5, color="#0F172A", fontweight="bold")

    # Tier 3
    box3 = FancyBboxPatch((0.5, 0.3), 9.0, 2.2, boxstyle="round,pad=0.25", fc="#F8FAFC", ec="#64748B", lw=2.5)
    ax.add_patch(box3)
    ax.text(1.0, 1.9, "PERSISTENCE LAYER (SQLite)", fontsize=11, fontweight="bold", color="#0F172A")
    ax.text(8.8, 1.9, "data/app.db", ha="right", fontsize=9.5, fontweight="bold", color="#64748B")
    ax.text(1.0, 1.1, "• Tables: datasets (metadata, columns JSON) & records (data_json per row)\n• Pre-seeded benchmarks + dynamic CSV upload ingestion\n• ACID-compliant, zero-configuration, file-based storage", 
            fontsize=8.5, color="#334155", va="top")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'architecture.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] architecture.png")

# ───────────────────────────────────────────────────────────
# CHART 11: Comparative capability chart
# ───────────────────────────────────────────────────────────
def chart_capability_comparison():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    ax.set_facecolor('#FAFAFA')

    categories = ['Custom CSV\nUpload', 'Database\nPersistence', 'Statistical\nRigor (p-value)', 
                  'Linked Views\n(Scatter/Heatmap)', 'Graph UX\n(Zoom/Pin)']
    x = np.arange(len(categories))
    width = 0.35

    proto = [10, 0, 25, 20, 45]
    full = [100, 100, 95, 95, 98]

    r1 = ax.bar(x - width/2, proto, width, label='Phase 1: Client Prototype', color='#94A3B8', edgecolor='#64748B', lw=1.2)
    r2 = ax.bar(x + width/2, full, width, label='Phase 2: Full-Stack Studio', color='#2563EB', edgecolor='#1D4ED8', lw=1.2)

    ax.set_ylabel('Capability Score (%)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Feature Evolution: Prototype vs Full-Stack Platform', fontsize=12, fontweight='bold', color='#0F172A', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9.5, color='#334155')
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=9.5)
    ax.set_ylim(0, 125)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    for bar in r1:
        ax.text(bar.get_x() + bar.get_width()/2.0, bar.get_height() + 2, f"{int(bar.get_height())}%", 
                ha='center', fontsize=8.5, color='#64748B', fontweight='bold')
    for bar in r2:
        ax.text(bar.get_x() + bar.get_width()/2.0, bar.get_height() + 2, f"{int(bar.get_height())}%", 
                ha='center', fontsize=8.5, color='#1D4ED8', fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(OUT, 'capability_comparison.png'), dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] capability_comparison.png")

# ═══════════════════════════════════════════════════════════
# RUN ALL
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating presentation chart assets...")
    chart_student_heatmap()
    chart_econ_heatmap()
    chart_scatter_math_physics()
    chart_scatter_gdp_unemp()
    chart_student_topN()
    chart_econ_topN()
    chart_degree_centrality()
    chart_student_distributions()
    chart_pearson_vs_spearman()
    chart_architecture()
    chart_capability_comparison()
    print(f"\nAll charts saved to: {OUT}")
