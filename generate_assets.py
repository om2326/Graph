import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

from matplotlib.patches import FancyBboxPatch

def make_slide4_arch():
    fig, ax = plt.subplots(figsize=(6, 5.5), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Card 1: Frontend
    box1 = FancyBboxPatch((0.8, 6.8), 8.4, 2.5, boxstyle="round,pad=0.2", fc="#EFF6FF", ec="#2563EB", lw=2)
    ax.add_patch(box1)
    ax.text(5.0, 8.5, "FRONTEND CLIENT TIER", ha="center", va="center", fontsize=11, fontweight="bold", color="#1E293B")
    ax.text(5.0, 7.7, "• D3.js Force-Directed Graph (Physics, Zoom, Pinning)\n• Correlation Heatmap Matrix & Scatter Modals", 
            ha="center", va="center", fontsize=9, color="#475569")

    # Arrow 1
    ax.annotate('', xy=(5.0, 6.7), xytext=(5.0, 6.0),
                arrowprops=dict(arrowstyle="<->", color="#2563EB", lw=2))
    ax.text(5.2, 6.35, "REST API (JSON)", fontsize=8, color="#2563EB", fontweight="bold")

    # Card 2: Backend
    box2 = FancyBboxPatch((0.8, 3.5), 8.4, 2.5, boxstyle="round,pad=0.2", fc="#F8FAFC", ec="#0F172A", lw=2)
    ax.add_patch(box2)
    ax.text(5.0, 5.2, "BACKEND COMPUTATION TIER", ha="center", va="center", fontsize=11, fontweight="bold", color="#1E293B")
    ax.text(5.0, 4.4, "• FastAPI Server & Uvicorn ASGI\n• SciPy Stats (Pearson, Spearman, p-values, OLS)", 
            ha="center", va="center", fontsize=9, color="#475569")

    # Arrow 2
    ax.annotate('', xy=(5.0, 3.4), xytext=(5.0, 2.7),
                arrowprops=dict(arrowstyle="<->", color="#0F172A", lw=2))
    ax.text(5.2, 3.05, "SQL / Queries", fontsize=8, color="#0F172A", fontweight="bold")

    # Card 3: Database
    box3 = FancyBboxPatch((0.8, 0.4), 8.4, 2.3, boxstyle="round,pad=0.2", fc="#F0FDF4", ec="#16A34A", lw=2)
    ax.add_patch(box3)
    ax.text(5.0, 1.9, "DATABASE PERSISTENCE TIER", ha="center", va="center", fontsize=11, fontweight="bold", color="#1E293B")
    ax.text(5.0, 1.2, "• SQLite Engine (app.db)\n• Tables: datasets, records (Persistent Storage)", 
            ha="center", va="center", fontsize=9, color="#475569")

    plt.tight_layout()
    plt.savefig("slide4_arch.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("Created slide4_arch.png")

def make_slide6_comparative():
    fig, ax = plt.subplots(figsize=(11.6, 4.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FAFAFA')

    categories = [
        'Data Ingestion\n& Upload', 
        'Database\nPersistence', 
        'Statistical Rigor\n(p-values & OLS)', 
        'Multi-View\nDrilldown', 
        'Centrality &\n централизация'
    ]
    categories = [
        'Data Upload\n(Custom CSV)',
        'Database\nPersistence',
        'Statistical Rigor\n(p-value & OLS)',
        'Linked Multi-View\n(Scatter/Heatmap)',
        'Graph Usability\n(Zoom, Pan, Pin)'
    ]
    
    x = np.arange(len(categories))
    width = 0.35

    v_proto = [15, 0, 30, 20, 45]
    v_full = [100, 100, 95, 95, 98]

    rects1 = ax.bar(x - width/2, v_proto, width, label='Phase 1: Client Prototype', color='#94A3B8', edgecolor='#64748B', lw=1.2, alpha=0.9)
    rects2 = ax.bar(x + width/2, v_full, width, label='Phase 2: Full-Stack Studio', color='#2563EB', edgecolor='#1D4ED8', lw=1.2)

    ax.set_ylabel('Capability Score (%)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Feature Capability & Rigor: Prototype vs. Full-Stack Platform', fontsize=13, fontweight='bold', color='#0F172A', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10, color='#334155')
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E2E8F0', fontsize=10)
    ax.set_ylim(0, 120)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')

    for bar in rects1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{int(yval)}%", ha='center', va='bottom', fontsize=9, color='#64748B', fontweight='bold')

    for bar in rects2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{int(yval)}%", ha='center', va='bottom', fontsize=9, color='#1D4ED8', fontweight='bold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.spines['bottom'].set_color('#CBD5E1')

    plt.tight_layout()
    plt.savefig("slide6_comparative.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("Created slide6_comparative.png")

def make_slide7_workflow():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.4), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')

    # Panel 1: Scatter plot & OLS Regression
    ax1.set_facecolor('#FAFAFA')
    np.random.seed(42)
    x = np.random.normal(70, 12, 100)
    noise = np.random.normal(0, 5, 100)
    y = 0.83 * x + 11.5 + noise

    ax1.scatter(x, y, color='#2563EB', alpha=0.7, edgecolors='#FFFFFF', s=45, label='Student Marks (N=100)')
    
    # Regression line
    line_x = np.linspace(min(x), max(x), 100)
    line_y = 0.83 * line_x + 11.5
    ax1.plot(line_x, line_y, color='#B5452D', lw=2.5, label='OLS Fit (r = 0.831, R² = 0.691)')

    ax1.set_title('Bivariate Scatter & OLS Linear Regression', fontsize=11, fontweight='bold', color='#0F172A')
    ax1.set_xlabel('Math Score', fontsize=10, color='#334155')
    ax1.set_ylabel('Physics Score', fontsize=10, color='#334155')
    ax1.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
    ax1.legend(loc='upper left', fontsize=8.5, frameon=True, facecolor='#FFFFFF')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Panel 2: Distribution of Correlations (Macroeconomic Dataset)
    ax2.set_facecolor('#FAFAFA')
    corrs = [-0.95, -0.88, -0.74, -0.62, -0.45, -0.32, -0.21, 0.15, 0.38, 0.52, 0.68, 0.84, 0.91]
    
    colors = ['#B5452D' if c < 0 else '#1C6E6E' for c in corrs]
    y_pos = np.arange(len(corrs))
    ax2.barh(y_pos, corrs, color=colors, height=0.65, edgecolor='#FFFFFF')
    ax2.set_yticks(y_pos)
    labels = [
        'GDP - Unemp', 'Unemp - Stocks', 'Rates - GDP', 'Infl - Conf',
        'Conf - Unemp', 'Infl - Stocks', 'Rates - Conf', 'GDP - Conf',
        'Stocks - GDP', 'Infl - Rates', 'Unemp - Infl', 'GDP - Stocks', 'Conf - Stocks'
    ]
    ax2.set_yticklabels(labels, fontsize=8, color='#334155')
    ax2.set_title('Correlation Distribution (Rust: Neg | Teal: Pos)', fontsize=11, fontweight='bold', color='#0F172A')
    ax2.set_xlabel('Correlation Coefficient (r)', fontsize=10, color='#334155')
    ax2.axvline(0, color='#64748B', lw=1)
    ax2.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig("slide7_workflow.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("Created slide7_workflow.png")

if __name__ == "__main__":
    make_slide4_arch()
    make_slide6_comparative()
    make_slide7_workflow()
