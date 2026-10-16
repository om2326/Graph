import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Arrow, FancyArrowPatch

# Matplotlib styling for high-res publication-grade assets
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']

def generate_arch_asset():
    fig, ax = plt.subplots(figsize=(6.2, 5.6), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Header / Title
    ax.text(5.0, 9.6, "SYSTEM ARCHITECTURE PIPELINE", ha="center", va="center", 
            fontsize=11, fontweight="bold", color="#0F172A")

    # Box 1: Frontend Client Tier
    box1 = FancyBboxPatch((0.6, 6.7), 8.8, 2.3, boxstyle="round,pad=0.25", fc="#F0FDF4", ec="#0D9488", lw=2)
    ax.add_patch(box1)
    ax.text(1.1, 8.4, "1. FRONTEND CLIENT TIER (Browser)", fontsize=10.5, fontweight="bold", color="#0F172A")
    ax.text(8.8, 8.4, "D3.js v7 • SVG", ha="right", fontsize=9, fontweight="bold", color="#0D9488")
    ax.text(1.1, 7.5, "• Force-Directed Graph: Physics, Drag, Zoom, Pinning\n• Dual Views: Correlation Heatmap Matrix & Scatter Modals\n• Inspector Panel: Dynamic Univariate Histograms", 
            fontsize=8.5, color="#334155", va="top")

    # Arrow 1: Bi-directional HTTP/JSON
    ax.annotate('', xy=(5.0, 6.6), xytext=(5.0, 5.8),
                arrowprops=dict(arrowstyle="<->", color="#2563EB", lw=2.2, mutation_scale=14))
    ax.text(5.2, 6.2, "REST API (JSON / Multipart)", fontsize=8, color="#2563EB", fontweight="bold")

    # Box 2: Backend Computation Tier
    box2 = FancyBboxPatch((0.6, 3.4), 8.8, 2.3, boxstyle="round,pad=0.25", fc="#EFF6FF", ec="#2563EB", lw=2)
    ax.add_patch(box2)
    ax.text(1.1, 5.1, "2. BACKEND COMPUTATION TIER (FastAPI)", fontsize=10.5, fontweight="bold", color="#0F172A")
    ax.text(8.8, 5.1, "Python 3.14 • SciPy", ha="right", fontsize=9, fontweight="bold", color="#2563EB")
    ax.text(1.1, 4.2, "• Statistical Engine: Pearson (r) & Spearman (ρ) Matrices\n• Hypothesis Testing: Two-Tailed Student t p-values\n• Linear Regression: OLS Trendline, R², & Distribution Bins", 
            fontsize=8.5, color="#334155", va="top")

    # Arrow 2: SQLite Query Bridge
    ax.annotate('', xy=(5.0, 3.3), xytext=(5.0, 2.5),
                arrowprops=dict(arrowstyle="<->", color="#0F172A", lw=2.2, mutation_scale=14))
    ax.text(5.2, 2.9, "SQL Queries & Schema Ingestion", fontsize=8, color="#0F172A", fontweight="bold")

    # Box 3: Persistence Database Tier
    box3 = FancyBboxPatch((0.6, 0.4), 8.8, 2.0, boxstyle="round,pad=0.25", fc="#F8FAFC", ec="#64748B", lw=2)
    ax.add_patch(box3)
    ax.text(1.1, 1.8, "3. PERSISTENCE DATABASE TIER (SQLite)", fontsize=10.5, fontweight="bold", color="#0F172A")
    ax.text(8.8, 1.8, "app.db • Zero Setup", ha="right", fontsize=9, fontweight="bold", color="#64748B")
    ax.text(1.1, 1.1, "• Relational Schema: datasets (metadata) & records (raw rows)\n• Pre-Seeded Presets: Student Performance & Macroeconomics\n• Custom CSV Ingestion: Dynamic feature isolation", 
            fontsize=8.5, color="#334155", va="top")

    plt.tight_layout()
    out_path = "asset_arch.png"
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path}")

def generate_comparison_asset():
    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    categories = [
        'Data Upload\n(Custom CSV)',
        'Database\nPersistence',
        'Statistical Rigor\n(p-value & OLS)',
        'Linked Multi-View\n(Scatter/Heatmap)',
        'Graph Usability\n(Zoom/Pan/Pin)'
    ]
    
    x = np.arange(len(categories))
    width = 0.35

    v_proto = [10, 0, 25, 20, 45]
    v_full = [100, 100, 95, 95, 98]

    rects1 = ax.bar(x - width/2, v_proto, width, label='Phase 1: Prototype', color='#94A3B8', edgecolor='#64748B', lw=1.2, alpha=0.9)
    rects2 = ax.bar(x + width/2, v_full, width, label='Phase 2: Full-Stack Studio', color='#2563EB', edgecolor='#1D4ED8', lw=1.2)

    ax.set_ylabel('Capability Score (%)', fontsize=10, fontweight='bold', color='#1E293B')
    ax.set_title('Feature Capability: Prototype vs. Full-Stack Platform', fontsize=11, fontweight='bold', color='#0F172A', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8.5, color='#334155')
    ax.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=8.5)
    ax.set_ylim(0, 130)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')

    for bar in rects1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2.5, f"{int(yval)}%", ha='center', va='bottom', fontsize=8, color='#64748B', fontweight='bold')

    for bar in rects2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2.5, f"{int(yval)}%", ha='center', va='bottom', fontsize=8, color='#1D4ED8', fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')

    plt.tight_layout()
    out_path = "asset_comparison.png"
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path}")

def generate_analytics_asset():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 3.6), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')

    # Panel 1: Scatter plot & OLS Regression
    ax1.set_facecolor('#FAFAFA')
    np.random.seed(42)
    x = np.random.normal(70, 12, 80)
    noise = np.random.normal(0, 4.5, 80)
    y = 0.83 * x + 11.5 + noise

    ax1.scatter(x, y, color='#2563EB', alpha=0.75, edgecolors='#FFFFFF', s=35, label='Observations (N=80)')
    
    line_x = np.linspace(min(x), max(x), 80)
    line_y = 0.83 * line_x + 11.5
    ax1.plot(line_x, line_y, color='#B5452D', lw=2.2, label='OLS Fit (r = 0.83, R² = 0.69)')

    ax1.set_title('Bivariate OLS Linear Regression', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax1.set_xlabel('Independent Variable (X)', fontsize=8, color='#334155')
    ax1.set_ylabel('Dependent Variable (Y)', fontsize=8, color='#334155')
    ax1.tick_params(labelsize=7.5)
    ax1.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
    ax1.legend(loc='upper left', fontsize=7.2, frameon=True, facecolor='#FFFFFF')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Panel 2: Distribution of Correlations (Macroeconomic Dataset)
    ax2.set_facecolor('#FAFAFA')
    corrs = [-0.95, -0.88, -0.74, -0.45, -0.21, 0.15, 0.52, 0.68, 0.84, 0.91]
    colors = ['#B5452D' if c < 0 else '#0D9488' for c in corrs]
    y_pos = np.arange(len(corrs))
    ax2.barh(y_pos, corrs, color=colors, height=0.65, edgecolor='#FFFFFF')
    ax2.set_yticks(y_pos)
    labels = [
        'GDP - Unemp', 'Unemp - Stocks', 'Rates - GDP', 'Conf - Unemp',
        'Rates - Conf', 'GDP - Conf', 'Unemp - Infl', 'Rates - Infl',
        'GDP - Stocks', 'Conf - Stocks'
    ]
    ax2.set_yticklabels(labels, fontsize=7, color='#334155')
    ax2.set_title('Correlation Matrix (Rust: Neg | Teal: Pos)', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax2.set_xlabel('Correlation Coefficient (r)', fontsize=8, color='#334155')
    ax2.tick_params(labelsize=7.5)
    ax2.axvline(0, color='#64748B', lw=1)
    ax2.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    out_path = "asset_analytics.png"
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path}")

def generate_physics_asset():
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(5.0, 6.7, "D3.js FORCE SIMULATION & ENCODINGS", ha="center", va="center", 
            fontsize=10.5, fontweight="bold", color="#0F172A")

    # Center Hub Node
    hub = Circle((3.2, 3.8), 0.95, facecolor='#0D9488', edgecolor='#0F766E', lw=2)
    ax.add_patch(hub)
    ax.text(3.2, 3.8, "Hub Variable\n(High Degree)", ha='center', va='center', fontsize=7.2, color='#FFFFFF', fontweight='bold')

    # Positive Partner (Strong +r, close spring distance)
    n_pos = Circle((6.8, 4.8), 0.75, facecolor='#2563EB', edgecolor='#1D4ED8', lw=2)
    ax.add_patch(n_pos)
    ax.text(6.8, 4.8, "Strong +r\n(Stem Core)", ha='center', va='center', fontsize=6.8, color='#FFFFFF', fontweight='bold')

    # Link 1: Teal Solid (Strong Positive)
    ax.plot([4.1, 6.1], [4.05, 4.6], color='#0D9488', lw=3.8, solid_capstyle='round')
    ax.text(5.1, 4.7, "+0.84 (Solid Teal)", ha='center', fontsize=7.5, color='#0D9488', fontweight='bold', rotation=15)

    # Negative Partner (Rust Dashed, inverse correlation)
    n_neg = Circle((7.2, 2.2), 0.75, facecolor='#B5452D', edgecolor='#991B1B', lw=2)
    ax.add_patch(n_neg)
    ax.text(7.2, 2.2, "Inverse -r\n(Unemp)", ha='center', va='center', fontsize=6.8, color='#FFFFFF', fontweight='bold')

    # Link 2: Rust Dashed (Strong Negative)
    ax.plot([4.05, 6.5], [3.45, 2.45], color='#B5452D', lw=3.2, linestyle='--', dashes=(4, 3))
    ax.text(5.3, 2.5, "-0.95 (Dashed Rust)", ha='center', fontsize=7.5, color='#B5452D', fontweight='bold', rotation=-22)

    # Annotations
    ax.text(5.0, 5.8, "• Spring Tension: Distance = 200 - |r| * 120 (Stronger r -> Shorter Link)", 
            ha='center', fontsize=7.5, color="#334155")
    ax.text(5.0, 0.7, "• ManyBody Repulsion (charge -320) & Collision prevent label overlap\n• Node Radius proportional to degree centrality sum(|r|)", 
            ha='center', fontsize=7.5, color="#475569")

    plt.tight_layout()
    out_path = "asset_physics.png"
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path}")

def generate_dataflow_asset():
    fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=220)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    ax.text(5.0, 8.1, "AUTOMATED CSV INGESTION & PIPELINE", ha="center", va="center", 
            fontsize=10.5, fontweight="bold", color="#0F172A")

    steps = [
        ("1. Multipart CSV Upload", "User drops any tabular .csv via interactive modal dialog", "#EFF6FF", "#2563EB"),
        ("2. Pandas Feature Isolation", "Extracts numeric features, removes empty/corrupt records", "#F0FDF4", "#0D9488"),
        ("3. SQLite Persistence Layer", "Assigns dataset UUID, stores column schemas & row observations", "#F8FAFC", "#64748B"),
        ("4. Topology & Cache Generation", "Calculates correlation matrices & p-values for instant UI rendering", "#FEF2F2", "#B5452D")
    ]

    y_start = 6.9
    y_gap = 1.7
    for i, (title, desc, fc, ec) in enumerate(steps):
        y = y_start - i * y_gap
        box = FancyBboxPatch((0.6, y - 0.45), 8.8, 1.15, boxstyle="round,pad=0.15", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(box)
        ax.text(1.0, y + 0.28, title, fontsize=9.2, fontweight="bold", color="#0F172A")
        ax.text(1.0, y - 0.12, desc, fontsize=7.8, color="#475569")
        
        if i < len(steps) - 1:
            ax.annotate('', xy=(5.0, y - 0.85), xytext=(5.0, y - 0.5),
                        arrowprops=dict(arrowstyle="->", color=ec, lw=2.0, mutation_scale=14))

    plt.tight_layout()
    out_path = "asset_dataflow.png"
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_arch_asset()
    generate_comparison_asset()
    generate_analytics_asset()
    generate_physics_asset()
    generate_dataflow_asset()
    print("All assets generated successfully!")
