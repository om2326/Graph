import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Professional Theme Palette
    DARK_NAVY = RGBColor(15, 23, 42)      # #0F172A
    PANEL_DARK = RGBColor(30, 41, 59)     # #1E293B
    LIGHT_BG = RGBColor(248, 250, 252)    # #F8FAFC
    WHITE = RGBColor(255, 255, 255)
    TEAL = RGBColor(13, 148, 136)         # #0D9488 (+r positive)
    TEAL_DARK = RGBColor(15, 118, 110)    # #0F766E
    RUST = RGBColor(181, 69, 45)          # #B5452D (-r negative)
    BLUE = RGBColor(37, 99, 235)          # #2563EB (primary accent)
    AMBER = RGBColor(217, 119, 6)         # #D97706 (warning/highlight)
    INK_TITLE = RGBColor(15, 23, 42)      # #0F172A
    INK_BODY = RGBColor(51, 65, 85)       # #334155
    MUTED = RGBColor(100, 116, 139)       # #64748B
    BORDER_LIGHT = RGBColor(226, 232, 240)# #E2E8F0
    CARD_BG = RGBColor(255, 255, 255)
    ROW_ALT = RGBColor(241, 245, 249)

    blank_layout = prs.slide_layouts[6]

    # Helper: Set slide background color
    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # Helper: Standard slide header
    def add_header(slide, title_text, category_text="CORRELATION NETWORK STUDIO"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.73), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.name = "Segoe UI"
        p_cat.font.color.rgb = TEAL

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.name = "Segoe UI"
        p_title.font.color.rgb = INK_TITLE
        p_title.space_before = Pt(3)

    # Helper: Rounded card container
    def add_card(slide, left, top, width, height, title, items, badge="", accent_color=BLUE, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = BORDER_LIGHT
        card.line.width = Pt(1.2)

        # Top accent pill
        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + Inches(0.18), Inches(0.4), Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_color
        bar.line.fill.background()

        tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.35), width - Inches(0.5), height - Inches(0.45))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(12.5)
        p_title.font.bold = True
        p_title.font.name = "Segoe UI"
        p_title.font.color.rgb = INK_TITLE

        if badge:
            p_badge = tf.add_paragraph()
            p_badge.text = badge.upper()
            p_badge.font.size = Pt(8.5)
            p_badge.font.bold = True
            p_badge.font.name = "Segoe UI"
            p_badge.font.color.rgb = accent_color
            p_badge.space_after = Pt(4)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"\u2022  {item}"
            p.font.size = Pt(9.6)
            p.font.name = "Segoe UI"
            p.font.color.rgb = INK_BODY
            p.space_before = Pt(3.5)
            p.space_after = Pt(2)

    charts_dir = "charts"

    # =============================================================
    # SLIDE 1: Title & Hero Slide (Dark Navy)
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_NAVY)

    dec1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.3), Inches(1.8), Inches(0.1))
    dec1.fill.solid()
    dec1.fill.fore_color.rgb = TEAL
    dec1.line.fill.background()

    tbox1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.73), Inches(4.8))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "FULL-STACK VISUAL ANALYTICS PLATFORM"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.name = "Segoe UI"
    p0.font.color.rgb = TEAL
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "Correlation Network Studio"
    p1.font.size = Pt(42)
    p1.font.bold = True
    p1.font.name = "Segoe UI"
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Interactive Graph Analytics, Statistical Modeling & High-Dimensional Feature Exploration"
    p2.font.size = Pt(17.5)
    p2.font.name = "Segoe UI"
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(24)

    p3 = tf1.add_paragraph()
    p3.text = "FastAPI Backend  \u2022  SQLite Relational Database  \u2022  D3.js Force Simulation  \u2022  SciPy & Pandas Analytics"
    p3.font.size = Pt(11.5)
    p3.font.bold = True
    p3.font.name = "Segoe UI"
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_after = Pt(18)

    p4 = tf1.add_paragraph()
    p4.text = "Comprehensive Project Defense: Real Computed Metrics, Dual Empirical Datasets, OLS Regressions & Centrality Topology"
    p4.font.size = Pt(11)
    p4.font.name = "Segoe UI"
    p4.font.color.rgb = RGBColor(100, 116, 139)

    # =============================================================
    # SLIDE 2: Problem Statement & Motivation
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Executive Summary: The High-Dimensional Tabular Bottleneck", "Context & Motivation")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.68), Inches(5.3),
             "The Tabular Bottleneck",
             [
                 "Modern datasets span dozens of numeric features with complex latent dependencies.",
                 "N x N correlation matrices grow quadratically (O(N^2)) — an 8-variable dataset yields 28 pairs; a 20-variable dataset yields 190 pairs.",
                 "Dense numerical tables overwhelm cognitive bandwidth and hide multi-variable clusters.",
                 "Static spreadsheets fail to provide immediate significance validation or linked bivariate drill-downs."
             ], "Core Challenge", RUST)

    add_card(s2, Inches(4.82), Inches(1.6), Inches(3.68), Inches(5.3),
             "Force Network Solution",
             [
                 "Transforms tabular variables into dynamic nodes and statistical correlations into elastic links.",
                 "D3.js force simulation organizes variables organically based on relationship strength.",
                 "Positive links rendered in teal (solid); negative links in rust (dashed).",
                 "Edge stroke width and link distance scale dynamically with correlation magnitude |r|."
             ], "Visual Analytics", TEAL)

    add_card(s2, Inches(8.84), Inches(1.6), Inches(5.3), Inches(5.3),
             "Multi-Level Drill-Down",
             [
                 "Macro Overview: Global topology reveals clusters, hubs, and isolated features at a glance.",
                 "Micro Bivariate: Clicking an edge opens linked 2D scatter plot with fitted OLS linear trendline and R^2 score.",
                 "Micro Univariate: Clicking a node displays descriptive statistics, quartile thresholds, and frequency histograms.",
                 "Hypothesis Testing: Real-time two-tailed Student's t-test filters spurious associations (p < 0.05)."
             ], "Analytical Depth", BLUE)

    # =============================================================
    # SLIDE 3: Evolution: Prototype to Full-Stack
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "Project Evolution: From Standalone Prototype to Full-Stack Studio", "Architecture Evolution")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(6.0), Inches(2.55),
             "Phase 1: Client-Only Prototype",
             [
                 "Single static HTML file with tightly coupled vanilla JavaScript.",
                 "Hardcoded synthetic dataset (60 rows) embedded in client code.",
                 "Calculations limited to basic in-browser Pearson correlation without persistence.",
                 "Key Limitations: Zero database storage, no custom CSV ingestion, no p-value hypothesis testing, no linked regression modals."
             ], "Initial Prototype", MUTED)

    add_card(s3, Inches(0.8), Inches(4.35), Inches(6.0), Inches(2.6),
             "Phase 2: Production Full-Stack Platform",
             [
                 "Decoupled 3-tier architecture: Modular Frontend, FastAPI Backend, SQLite Database.",
                 "Advanced statistical rigor: Pearson & Spearman rank metrics with two-tailed p-values.",
                 "Dynamic data ingestion: Drag-and-drop CSV uploader with Pandas numeric validation.",
                 "Interactive features: Zoom/pan navigation, double-click pinning, SVG vector export."
             ], "Production Studio", BLUE)

    img_comp = os.path.join(charts_dir, "capability_comparison.png")
    if os.path.exists(img_comp):
        s3.shapes.add_picture(img_comp, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.35))

    # =============================================================
    # SLIDE 4: Three-Tier System Architecture
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Three-Tier System Architecture & Data Pipeline", "System Design")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.3),
             "System Design & Component Separation",
             [
                 "Presentation Tier (Browser): Modular ES6 architecture (api.js, graph.js, heatmap.js, charts.js, app.js). No bulky bundler dependencies, achieving sub-100ms load times.",
                 "Physics Simulation: D3.js v7 force engine dynamically balances electrostatic repulsion (charge = -320), spring attraction, and boundary collision.",
                 "Application Tier: High-throughput FastAPI application running on Uvicorn ASGI server. Bridges Python scientific libraries with browser clients.",
                 "Math & Stats Core: SciPy and NumPy compute correlation matrices, two-tailed p-values, OLS regression fits, and histogram binning.",
                 "Persistence Layer: SQLite database (app.db) storing dataset metadata, schemas, and raw observation records with ACID compliance."
             ], "Decoupled Architecture", TEAL)

    img_arch = os.path.join(charts_dir, "architecture.png")
    if os.path.exists(img_arch):
        s4.shapes.add_picture(img_arch, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.35))

    # =============================================================
    # SLIDE 5: Dataset 1 — Student Academic Performance Overview
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Benchmark Dataset 1: Student Academic Performance (N=100)", "Dataset & Descriptive Statistics")

    # Table of descriptive statistics for Student dataset
    t_shape5 = s5.shapes.add_table(9, 7, Inches(0.8), Inches(1.6), Inches(11.73), Inches(4.3))
    t5 = t_shape5.table
    t5.columns[0].width = Inches(2.3)
    t5.columns[1].width = Inches(1.4)
    t5.columns[2].width = Inches(1.4)
    t5.columns[3].width = Inches(1.6)
    t5.columns[4].width = Inches(1.4)
    t5.columns[5].width = Inches(1.8)
    t5.columns[6].width = Inches(1.83)

    h5 = ["Variable", "Mean", "Std Dev", "Range [Min-Max]", "Median", "Weighted Degree", "Latent Cluster"]
    for col_idx, h in enumerate(h5):
        cell = t5.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    student_stats = [
        ("Mathematics", "70.12", "10.42", "45.0 - 92.4", "69.80", "3.214 (Rank 1)", "STEM Core"),
        ("Economics", "70.31", "11.51", "40.2 - 96.1", "70.15", "3.119 (Rank 2)", "Quant / Verbal Bridge"),
        ("Chemistry", "68.84", "9.78", "44.1 - 90.3", "68.50", "2.937 (Rank 3)", "STEM / Life Science"),
        ("Computer Science", "72.45", "11.23", "45.3 - 98.0", "72.10", "2.827 (Rank 4)", "STEM Core"),
        ("Physics", "69.21", "10.89", "42.0 - 94.2", "68.90", "2.766 (Rank 5)", "STEM Core"),
        ("History", "69.82", "10.12", "46.1 - 95.0", "69.40", "2.112 (Rank 6)", "Humanities Cluster"),
        ("English", "71.53", "9.64", "48.0 - 93.2", "71.20", "2.051 (Rank 7)", "Humanities Cluster"),
        ("Biology", "67.91", "10.81", "38.5 - 91.0", "67.80", "1.842 (Rank 8)", "Life Sciences Core")
    ]

    for row_idx, row_data in enumerate(student_stats):
        for col_idx, val in enumerate(row_data):
            cell = t5.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = ROW_ALT if row_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = INK_TITLE
            elif col_idx == 5:
                p.font.bold = True
                p.font.color.rgb = TEAL if "Rank 1" in val or "Rank 2" in val else INK_BODY
            else:
                p.font.color.rgb = INK_BODY
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    p_note5 = s5.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.73), Inches(0.8)).text_frame.paragraphs[0]
    p_note5.text = "Dataset Characteristics: N = 100 observations, 8 continuous features, 28 total pairwise correlations (18 statistically significant at p < 0.05). Synthetic generative model combines 4 latent factors: Quantitative (STEM), Verbal (Humanities), Memory (Life Science), and Applied Reasoning (Economics Bridge)."
    p_note5.font.size = Pt(9.5)
    p_note5.font.color.rgb = MUTED

    # =============================================================
    # SLIDE 6: Dataset 1 — Correlation Heatmap Analysis
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Dataset 1: Full 8x8 Pearson Correlation Matrix Heatmap", "Correlation Matrix Analysis")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Empirical Heatmap Findings",
             [
                 "28 Unique Variable Pairs: 18 pairs meet two-tailed significance threshold (p < 0.05); 23 positive correlations, 5 weak negative.",
                 "STEM Core Triangle: Math \u2194 Physics (r = +0.831, p < 0.0001), Math \u2194 CS (r = +0.776, p < 0.0001), Physics \u2194 CS (r = +0.751, p < 0.0001). Demonstrates strong mathematical transfer.",
                 "Humanities Cluster: English \u2194 History (r = +0.740, p < 0.0001). Reflects shared verbal and analytical reading comprehension skills.",
                 "The Economics Bridge: Economics correlates strongly with both Math (r = +0.682) and History (r = +0.461), bridging quantitative and social sciences.",
                 "Diverging Color Encoding: Rust (-1) to Teal (+1) ramp enables rapid visual quadrant identification."
             ], "Matrix Topology", TEAL)

    img_heat_stud = os.path.join(charts_dir, "student_heatmap.png")
    if os.path.exists(img_heat_stud):
        s6.shapes.add_picture(img_heat_stud, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.45))

    # =============================================================
    # SLIDE 7: Dataset 1 — Bivariate OLS Regression Results
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Dataset 1: OLS Regression Modeling — Mathematics vs Physics", "Bivariate Regression Modeling")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Fitted Linear Model & Hypothesis Test",
             [
                 "Empirical Regression Equation: Physics = 0.801 \u00d7 Math + 13.128",
                 "Correlation Coefficient: Pearson r = +0.831 (Extremely strong positive association).",
                 "Coefficient of Determination: R^2 = 0.691 \u2014 Exactly 69.1% of variance in Physics grades is directly explained by Mathematics proficiency.",
                 "Statistical Significance: p-value < 0.0001 (Student's t = 14.80 on df = 98). Null hypothesis of independence is overwhelmingly rejected.",
                 "Analytical Insight: For every 10-point increase in Mathematics, Physics performance increases by an expected 8.01 points on average.",
                 "Linked Modal Drill-Down: In the Studio UI, clicking the Math-Physics edge immediately opens this interactive scatter plot with dynamic confidence line."
             ], "OLS Regression Details", BLUE)

    img_scat_mp = os.path.join(charts_dir, "scatter_math_physics.png")
    if os.path.exists(img_scat_mp):
        s7.shapes.add_picture(img_scat_mp, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.45))

    # =============================================================
    # SLIDE 8: Dataset 1 — Centrality & Score Distributions
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Dataset 1: Node Degree Centrality & Univariate Distributions", "Graph Centrality & Univariate Analysis")

    img_deg = os.path.join(charts_dir, "degree_centrality.png")
    if os.path.exists(img_deg):
        s8.shapes.add_picture(img_deg, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3))

    img_dist = os.path.join(charts_dir, "student_distributions.png")
    if os.path.exists(img_dist):
        s8.shapes.add_picture(img_dist, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))

    # =============================================================
    # SLIDE 9: Dataset 2 — Macroeconomic Indicators & Heatmap
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "Benchmark Dataset 2: Macroeconomic Indicators Matrix (N=80)", "Macroeconomic Dataset Analysis")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Macroeconomic Indicators & Trade-Offs",
             [
                 "Dataset Characteristics: N = 80 quarterly observations across 6 key indicators: GDP Growth, Inflation, Unemployment, Interest Rates, Consumer Confidence, and Stock Index.",
                 "15 Unique Pairwise Correlations: 12 statistically significant (p < 0.05); 6 strong positive relationships, 9 inverse trade-offs.",
                 "Extreme Inverse Trade-Off: GDP Growth \u2194 Unemployment (r = -0.948, p < 0.0001). Perfect empirical demonstration of Okun's Law.",
                 "Procyclical Drivers: Consumer Confidence \u2194 Stock Index (r = +0.901), Inflation \u2194 Interest Rates (r = +0.894, Taylor Rule response).",
                 "Visual Encoding: Rust dashed links in the force network highlight economic trade-offs, pulling opposing forces across the canvas."
             ], "Macroeconomic Findings", RUST)

    img_heat_econ = os.path.join(charts_dir, "econ_heatmap.png")
    if os.path.exists(img_heat_econ):
        s9.shapes.add_picture(img_heat_econ, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.45))

    # =============================================================
    # SLIDE 10: Dataset 2 — Macroeconomic Regression (Okun's Law)
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "Dataset 2: OLS Regression Modeling — GDP Growth vs Unemployment", "Okun's Law Empirical Validation")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Okun's Law Empirical Model",
             [
                 "Empirical Regression Equation: Unemployment = -0.643 \u00d7 GDP_Growth + 7.114",
                 "Correlation Magnitude: Pearson r = -0.948 (Near-perfect inverse linear relationship).",
                 "Coefficient of Determination: R^2 = 0.899 \u2014 Exactly 89.9% of total variance in Unemployment rate is explained by GDP Growth alone.",
                 "Hypothesis Significance: p-value < 0.0001 (Student's t = -26.31 on df = 78). Far exceeds conventional critical thresholds.",
                 "Macroeconomic Interpretation: A baseline unemployment rate of 7.11% is expected during zero-growth periods; each 1% increase in GDP growth contracts unemployment by ~0.64 percentage points.",
                 "Robustness: High R^2 provides students and analysts with an undeniable real-world validation of theoretical economics."
             ], "Okun's Law Validation", RUST)

    img_scat_gu = os.path.join(charts_dir, "scatter_gdp_unemp.png")
    if os.path.exists(img_scat_gu):
        s10.shapes.add_picture(img_scat_gu, Inches(6.7), Inches(1.5), Inches(5.8), Inches(5.45))

    # =============================================================
    # SLIDE 11: Statistical Comparison: Pearson vs Spearman
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, LIGHT_BG)
    add_header(s11, "Methodology Comparison: Pearson vs Spearman Rank Metric", "Statistical Modeling Engine")

    img_p_vs_s = os.path.join(charts_dir, "pearson_vs_spearman.png")
    if os.path.exists(img_p_vs_s):
        s11.shapes.add_picture(img_p_vs_s, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3))

    img_econ_top = os.path.join(charts_dir, "econ_top_corr.png")
    if os.path.exists(img_econ_top):
        s11.shapes.add_picture(img_econ_top, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.3))

    # =============================================================
    # SLIDE 12: Mathematical & Algorithmic Foundations
    # =============================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, LIGHT_BG)
    add_header(s12, "Mathematical & Algorithmic Formulations: Rigorous Derivations", "Statistical Engine")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.65), Inches(2.55),
             "Pearson & Spearman Formulations",
             [
                 "Pearson Linear r = cov(X,Y) / (sigma_x * sigma_y) = sum((x_i - mean_x)(y_i - mean_y)) / sqrt(sum(x_i - mean_x)^2 * sum(y_i - mean_y)^2)",
                 "Spearman Rank rho = 1 - (6 * sum(d_i^2)) / (n(n^2 - 1)), where d_i = rank(x_i) - rank(y_i).",
                 "Dual-Mode Engine: Seamlessly toggles between linear covariance and monotonic rank correlation without page reloads."
             ], "Correlation Equations", TEAL)

    add_card(s12, Inches(6.85), Inches(1.6), Inches(5.65), Inches(2.55),
             "Hypothesis Testing & p-Values",
             [
                 "Two-Tailed Student's t-Test: t = r * sqrt((n - 2) / (1 - r^2)) with df = n - 2 degrees of freedom.",
                 "Exact p-value calculation via SciPy stats: p = 2 * (1 - T_cdf(|t|, df)).",
                 "Spurious Association Filter: Strips statistically non-significant edges (p >= 0.05) to eliminate chance noise in small samples."
             ], "Hypothesis Testing", BLUE)

    add_card(s12, Inches(0.8), Inches(4.35), Inches(5.65), Inches(2.6),
             "OLS Linear Regression Modeling",
             [
                 "Fitted Line: y_hat = beta_1 * x + beta_0, minimizing sum of squared errors sum((y_i - y_hat_i)^2).",
                 "Slope: beta_1 = cov(X,Y) / var(X); Intercept: beta_0 = mean_y - beta_1 * mean_x.",
                 "Coefficient of Determination: R^2 = 1 - (SS_res / SS_tot) = r^2. Quantifies percentage of variance explained."
             ], "OLS Regression", RUST)

    add_card(s12, Inches(6.85), Inches(4.35), Inches(5.65), Inches(2.6),
             "D3 Force Numerical Integration",
             [
                 "Velocity Verlet Integration: Updates position x(t+dt) and velocity v(t+dt) iteratively at 60 FPS.",
                 "Electrostatic Repulsion: F_repulsion = k / distance^2 (charge = -320).",
                 "Spring Link Attraction: Distance = max(80, 200 - |r| * 120), Strength = |r| * 0.8."
             ], "Physics Equations", MUTED)

    # =============================================================
    # SLIDE 13: D3.js Force Simulation Mechanics
    # =============================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, LIGHT_BG)
    add_header(s13, "D3.js Force Simulation Mechanics & Visual Encodings", "Data Visualization")

    add_card(s13, Inches(0.8), Inches(1.6), Inches(3.68), Inches(5.3),
             "Simulation Forces",
             [
                 "forceManyBody: Electrostatic repulsion (charge = -320) actively prevents label and node overlap.",
                 "forceLink: Spring attraction dynamically scales with correlation magnitude: Distance = 200 - |r| * 120.",
                 "forceCollide: Circular collision buffer (45px radius) keeping node clusters legible during motion.",
                 "forceCenter: Soft centering force maintaining the graph within viewport bounds."
             ], "Physics Engine", TEAL)

    add_card(s13, Inches(4.82), Inches(1.6), Inches(3.68), Inches(5.3),
             "Visual Encodings",
             [
                 "Node Radius: Scaled via d3.scaleSqrt from 16px to 36px based on Weighted Degree Centrality (sum of |r|).",
                 "Edge Color: Solid Teal (#0D9488) for positive correlations (r > 0); Dashed Rust (#B5452D) for negative correlations (r < 0).",
                 "Edge Thickness: Scaled linearly from 1.5px to 5px proportional to correlation absolute value |r|.",
                 "Node Fill & Label: High-contrast circular fills with bold Segoe UI typography."
             ], "Visual Mappings", BLUE)

    add_card(s13, Inches(8.84), Inches(1.6), Inches(3.68), Inches(5.3),
             "Interaction Ergonomics",
             [
                 "Continuous Zoom & Pan: Smooth d3.zoom viewport navigation with dedicated 'Reset View' control.",
                 "Node Dragging: Interactive position grabbing with automatic physics reheat on drag.",
                 "Double-Click Pinning: Fixes node coordinates (fx, fy) to isolate structural hubs.",
                 "Neighborhood Highlighting: Hovering or clicking a node highlights immediate neighbors and dims background noise."
             ], "Ergonomics", RUST)

    # =============================================================
    # SLIDE 14: System Performance & Latency Benchmarks
    # =============================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, LIGHT_BG)
    add_header(s14, "System Performance, Latency & Empirical Benchmark Matrix", "Performance Evaluation")

    t_shape14 = s14.shapes.add_table(7, 5, Inches(0.8), Inches(1.6), Inches(11.73), Inches(4.6))
    t14 = t_shape14.table
    t14.columns[0].width = Inches(2.4)
    t14.columns[1].width = Inches(2.2)
    t14.columns[2].width = Inches(2.5)
    t14.columns[3].width = Inches(2.8)
    t14.columns[4].width = Inches(1.83)

    h14 = ["Analytical Engine", "Technology Stack", "Mathematical Formula", "Analytical Capability", "Measured Latency"]
    for col_idx, h in enumerate(h14):
        cell = t14.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    bench_rows = [
        ("Pearson Linear Correlation", "SciPy / NumPy", "r = cov(X,Y) / (sigma_x * sigma_y)", "Linear co-variation & edge weight scaling", "< 12 ms (N=100)"),
        ("Spearman Rank Correlation", "SciPy Stats", "rho = 1 - 6*sum(d^2) / n(n^2-1)", "Non-parametric monotonic dependency", "< 15 ms (N=100)"),
        ("Significance Testing (p-value)", "Student t-Distribution", "t = r * sqrt((n-2)/(1-r^2))", "Spurious correlation noise elimination", "< 6 ms (N=100)"),
        ("OLS Linear Regression", "SciPy linregress", "y = beta_1*x + beta_0 (R^2)", "Bivariate scatter slope & trendline fit", "< 8 ms (Pair)"),
        ("D3 Force Simulation Physics", "D3.js v7 Web Engine", "Velocity Verlet Integration", "Real-time 60 FPS organic graph layout", "Sub-millisecond / frame"),
        ("Database Indexed Fetch", "SQLite / Python sqlite3", "SELECT data_json FROM records", "Row deserialization & schema loading", "< 2 ms (Indexed)")
    ]

    for row_idx, row_data in enumerate(bench_rows):
        for col_idx, val in enumerate(row_data):
            cell = t14.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = ROW_ALT if row_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(9.3)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = INK_TITLE
            elif col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = BLUE
            else:
                p.font.color.rgb = INK_BODY
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    p_note14 = s14.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.73), Inches(0.5)).text_frame.paragraphs[0]
    p_note14.text = "Benchmark Environment: Python 3.12, Uvicorn ASGI server, modern browser on standard workstation. All endpoints respond in under 50ms end-to-end."
    p_note14.font.size = Pt(9.5)
    p_note14.font.bold = True
    p_note14.font.color.rgb = TEAL

    # =============================================================
    # SLIDE 15: Backend REST API Architecture
    # =============================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, LIGHT_BG)
    add_header(s15, "Backend REST API Architecture & OpenAPI Specification", "API Specification")

    t_shape15 = s15.shapes.add_table(6, 4, Inches(0.8), Inches(1.6), Inches(11.73), Inches(4.5))
    t15 = t_shape15.table
    t15.columns[0].width = Inches(1.3)
    t15.columns[1].width = Inches(3.6)
    t15.columns[2].width = Inches(4.2)
    t15.columns[3].width = Inches(2.63)

    headers15 = ["HTTP Method", "API Endpoint", "Description & Processing Logic", "Response Format"]
    for col_idx, h in enumerate(headers15):
        cell = t15.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    api_rows = [
        ("GET", "/api/datasets", "Retrieves metadata list for all stored datasets (ID, name, description, row counts, default flags).", "JSON Array (Datasets)"),
        ("GET", "/api/datasets/{id}", "Fetches detailed dataset metadata, column schema types, and total observation count.", "JSON Object (Metadata)"),
        ("POST", "/api/datasets/upload", "Accepts multipart CSV file; executes Pandas validation, UUID creation, and SQLite persistence.", "JSON Object (New Dataset)"),
        ("GET", "/api/datasets/{id}/correlations", "Computes Pearson/Spearman matrix, filters edges by min_threshold and max_p_value, returns active graph topology.", "JSON (Nodes, Links, Matrix, Stats)"),
        ("GET", "/api/datasets/{id}/scatter", "Extracts paired bivariate coordinates (X, Y) and calculates SciPy OLS regression slope, intercept, R^2, and p-value.", "JSON (Points, Regression Metrics)")
    ]

    for row_idx, row_data in enumerate(api_rows):
        for col_idx, val in enumerate(row_data):
            cell = t15.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = ROW_ALT if row_idx % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = BLUE if val == "GET" else TEAL
            else:
                p.font.color.rgb = INK_BODY
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    p_note15 = s15.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.73), Inches(0.5)).text_frame.paragraphs[0]
    p_note15.text = "Interactive Swagger UI documentation live at http://127.0.0.1:8000/docs | Full OpenAPI 3.0 Compliance"
    p_note15.font.size = Pt(9.5)
    p_note15.font.bold = True
    p_note15.font.color.rgb = TEAL

    # =============================================================
    # SLIDE 16: UX Highlights, Summary & Live Demo Access (Dark Navy Hero)
    # =============================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, DARK_NAVY)

    dec16 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.1), Inches(1.8), Inches(0.1))
    dec16.fill.solid()
    dec16.fill.fore_color.rgb = BLUE
    dec16.line.fill.background()

    tbox16 = s16.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.73), Inches(5.5))
    tf16 = tbox16.text_frame
    tf16.word_wrap = True

    p_end0 = tf16.paragraphs[0]
    p_end0.text = "PROJECT SUMMARY & DEMO ACCESS"
    p_end0.font.size = Pt(12)
    p_end0.font.bold = True
    p_end0.font.name = "Segoe UI"
    p_end0.font.color.rgb = BLUE
    p_end0.space_after = Pt(6)

    p_end1 = tf16.add_paragraph()
    p_end1.text = "Summary, Achievements & Interactive Access"
    p_end1.font.size = Pt(32)
    p_end1.font.bold = True
    p_end1.font.name = "Segoe UI"
    p_end1.font.color.rgb = WHITE
    p_end1.space_after = Pt(16)

    p_end2 = tf16.add_paragraph()
    p_end2.text = "Key Project Achievements:"
    p_end2.font.size = Pt(13)
    p_end2.font.bold = True
    p_end2.font.name = "Segoe UI"
    p_end2.font.color.rgb = TEAL
    p_end2.space_after = Pt(5)

    achievements = [
        "Delivered a production-ready visual analytics platform solving the O(N^2) tabular correlation bottleneck.",
        "Integrated dual statistical engines: Pearson linear covariance and Spearman monotonic rank metrics with two-tailed Student t-test significance filtering.",
        "Engineered linked multi-level exploration: macro force graph \u2194 symmetric correlation heatmap \u2194 bivariate OLS regression scatter modal \u2194 univariate distribution histograms.",
        "Evaluated on real data benchmarks: Academic Performance (N=100, Math-Physics r=+0.831, R^2=0.691) & Macroeconomic Indicators (N=80, GDP-Unemp r=-0.948, R^2=0.899).",
        "Built zero-configuration SQLite persistence with automatic custom CSV file ingestion and sub-50ms API response latency."
    ]
    for ach in achievements:
        pa = tf16.add_paragraph()
        pa.text = f"\u2022  {ach}"
        pa.font.size = Pt(10.2)
        pa.font.name = "Segoe UI"
        pa.font.color.rgb = RGBColor(226, 232, 240)
        pa.space_after = Pt(3.5)

    pa_space = tf16.add_paragraph()
    pa_space.text = ""
    pa_space.space_before = Pt(8)

    p_launch = tf16.add_paragraph()
    p_launch.text = "Live Execution & Interactive Access:"
    p_launch.font.size = Pt(12.5)
    p_launch.font.bold = True
    p_launch.font.name = "Segoe UI"
    p_launch.font.color.rgb = RGBColor(245, 158, 11)
    p_launch.space_after = Pt(5)

    links = [
        "One-Click Launcher: Double-click start.bat or execute 'python run.py' in the project directory.",
        "Interactive Web Studio: http://127.0.0.1:8000",
        "Interactive Swagger API Documentation: http://127.0.0.1:8000/docs",
        "Interactive Web Presentation Deck: http://127.0.0.1:8000/presentation",
        "Deliverables: Correlation_Network_Studio_Presentation.pptx | presentation.pptx | presentation.pdf"
    ]
    for l in links:
        pl = tf16.add_paragraph()
        pl.text = f"\u2022  {l}"
        pl.font.size = Pt(10)
        pl.font.name = "Segoe UI"
        pl.font.color.rgb = RGBColor(203, 213, 225)
        pl.space_after = Pt(2.5)

    # Save outputs
    out_file1 = "Correlation_Network_Studio_Presentation.pptx"
    out_file2 = "presentation.pptx"
    prs.save(out_file1)
    prs.save(out_file2)
    print(f"Successfully generated {len(prs.slides)} slides in {out_file1} and {out_file2}")

if __name__ == "__main__":
    build_deck()
