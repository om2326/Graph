import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def build_presentation():
    base_ppt = "Predictive Analytics Presentation.pptx"
    out_ppt = "correlation_network_presentation.pptx"
    
    prs = Presentation(base_ppt)
    
    # -----------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -----------------------------------------------------------------
    s1 = prs.slides[0]
    for shape in s1.shapes:
        if shape.name == "TextBox 2":
            p = shape.text_frame.paragraphs[0]
            p.text = "Correlation Network Studio"
            if len(p.runs) > 0:
                p.runs[0].font.size = Pt(44)
                p.runs[0].font.bold = True
                p.runs[0].font.name = "Poppins"
        elif shape.name == "TextBox 4":
            shape.text_frame.text = ""
            p1 = shape.text_frame.paragraphs[0]
            p1.text = "Interactive Graph Analytics & Statistical Modeling Platform"
            p1.font.size = Pt(16)
            p1.font.name = "Inter"
            p1.font.color.rgb = RGBColor(100, 116, 139)
            p2 = shape.text_frame.add_paragraph()
            p2.text = "Full-Stack System: FastAPI • SQLite • D3.js Force Simulation • SciPy"
            p2.font.size = Pt(13)
            p2.font.name = "Inter"
            p2.font.bold = True
            p2.font.color.rgb = RGBColor(37, 99, 235)

    # -----------------------------------------------------------------
    # SLIDE 2: Preface & Objective
    # -----------------------------------------------------------------
    s2 = prs.slides[1]
    for shape in s2.shapes:
        if shape.name == "TextBox 2":
            shape.text_frame.text = "Preface &\nObjective"
            for p in shape.text_frame.paragraphs:
                p.font.name = "Poppins"
                p.font.size = Pt(40)
                p.font.bold = True
                p.font.color.rgb = RGBColor(37, 99, 235)
        elif shape.name == "TextBox 3":
            shape.text_frame.text = ""
            p = shape.text_frame.paragraphs[0]
            r1 = p.add_run()
            r1.text = "The Challenge: "
            r1.font.bold = True
            r1.font.name = "Inter"
            r1.font.size = Pt(14.5)
            r1.font.color.rgb = RGBColor(30, 41, 59)
            r2 = p.add_run()
            r2.text = "High-dimensional tabular datasets obscure cross-variable correlations. Traditional correlation matrices scale quadratically (N × N), making it difficult for analysts to discover clusters, hub variables, and inverse dependencies from raw numbers."
            r2.font.name = "Inter"
            r2.font.size = Pt(14.5)
            r2.font.color.rgb = RGBColor(71, 85, 105)
        elif shape.name == "TextBox 4":
            shape.text_frame.text = ""
            p = shape.text_frame.paragraphs[0]
            r1 = p.add_run()
            r1.text = "Our Objective: "
            r1.font.bold = True
            r1.font.name = "Inter"
            r1.font.size = Pt(14.5)
            r1.font.color.rgb = RGBColor(30, 41, 59)
            r2 = p.add_run()
            r2.text = "To engineer and deploy a full-stack visual analytics platform transforming raw numerical datasets into interactive, force-directed network graphs with linked bivariate regression scatter plots and univariate distribution metrics."
            r2.font.name = "Inter"
            r2.font.size = Pt(14.5)
            r2.font.color.rgb = RGBColor(71, 85, 105)
        elif shape.name == "TextBox 5":
            shape.text_frame.text = ""
            p = shape.text_frame.paragraphs[0]
            r1 = p.add_run()
            r1.text = "The Scope: "
            r1.font.bold = True
            r1.font.name = "Inter"
            r1.font.size = Pt(14.5)
            r1.font.color.rgb = RGBColor(30, 41, 59)
            r2 = p.add_run()
            r2.text = "This presentation outlines our decoupled three-tier architecture (FastAPI, SQLite, D3.js), the mathematical correlation engines (Pearson & Spearman with p-value validation), and the multi-level analytical user workflow."
            r2.font.name = "Inter"
            r2.font.size = Pt(14.5)
            r2.font.color.rgb = RGBColor(71, 85, 105)

    # -----------------------------------------------------------------
    # SLIDE 3: Methodology: The Core Pipeline
    # -----------------------------------------------------------------
    s3 = prs.slides[2]
    for shape in s3.shapes:
        if shape.name == "TextBox 17":
            shape.text_frame.text = "Methodology: The Core Pipeline"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(30)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 6":
            shape.text_frame.text = "1. Data Ingestion & Storage"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(17)
            shape.text_frame.paragraphs[0].font.bold = True
        elif shape.name == "TextBox 7":
            shape.text_frame.text = "Aggregated and structured multi-feature datasets in SQLite. Supports dynamic schema validation, automated CSV file ingestion, numeric feature isolation, and persistent row storage."
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(13)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(71, 85, 105)
        elif shape.name == "TextBox 9":
            shape.text_frame.text = "2. Statistical Engine"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(17)
            shape.text_frame.paragraphs[0].font.bold = True
        elif shape.name == "TextBox 10":
            shape.text_frame.text = "Engineered Pearson and Spearman correlation matrices with SciPy. Computed two-tailed Student t-distribution p-values and ordinary least squares (OLS) linear regressions."
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(13)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(71, 85, 105)
        elif shape.name == "TextBox 12":
            shape.text_frame.text = "3. Visual Analytics"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(17)
            shape.text_frame.paragraphs[0].font.bold = True
        elif shape.name == "TextBox 13":
            shape.text_frame.text = "Built D3.js force-directed network simulation with dynamic link tension, degree centrality node sizing, dual-mode correlation heatmap, and linked drill-down modals."
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(13)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(71, 85, 105)

    # -----------------------------------------------------------------
    # SLIDE 4: Architecture & Computation Engine
    # -----------------------------------------------------------------
    s4 = prs.slides[3]
    for shape in s4.shapes:
        if shape.name == "TextBox 9":
            shape.text_frame.text = "Architecture: Three-Tier System Design"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(30)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 3":
            shape.text_frame.text = "To establish a high-performance visual analytics workflow, we deployed a decoupled three-tier architecture bridging Python scientific computation with web-native D3.js physics."
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(13.5)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(71, 85, 105)
        elif shape.name == "TextBox 4":
            shape.text_frame.text = ""
            p = shape.text_frame.paragraphs[0]
            r1 = p.add_run()
            r1.text = "FastAPI Backend Service: "
            r1.font.bold = True
            r1.font.name = "Inter"
            r1.font.color.rgb = RGBColor(30, 41, 59)
            r2 = p.add_run()
            r2.text = "High-throughput asynchronous API layer exposing REST endpoints for graph topology, correlation matrices, and CSV upload."
            r2.font.name = "Inter"
            r2.font.color.rgb = RGBColor(71, 85, 105)
        elif shape.name == "TextBox 5":
            shape.text_frame.text = ""
            p = shape.text_frame.paragraphs[0]
            r1 = p.add_run()
            r1.text = "SciPy & NumPy Math Core: "
            r1.font.bold = True
            r1.font.name = "Inter"
            r1.font.color.rgb = RGBColor(30, 41, 59)
            r2 = p.add_run()
            r2.text = "Computes Pearson and Spearman matrices, two-tailed p-values for statistical significance, and OLS linear regression."
            r2.font.name = "Inter"
            r2.font.color.rgb = RGBColor(71, 85, 105)
        elif shape.name == "TextBox 6":
            shape.text_frame.text = ""
            p = shape.text_frame.paragraphs[0]
            r1 = p.add_run()
            r1.text = "D3.js Force Simulation: "
            r1.font.bold = True
            r1.font.name = "Inter"
            r1.font.color.rgb = RGBColor(30, 41, 59)
            r2 = p.add_run()
            r2.text = "Physics-based graph rendering with dynamic link attraction, electrostatic repulsion, zoom/pan navigation, and node pinning."
            r2.font.name = "Inter"
            r2.font.color.rgb = RGBColor(71, 85, 105)
        elif shape.name == "TextBox 7":
            shape.text_frame.text = ""
            p = shape.text_frame.paragraphs[0]
            r1 = p.add_run()
            r1.text = "SQLite Persistence Layer: "
            r1.font.bold = True
            r1.font.name = "Inter"
            r1.font.color.rgb = RGBColor(30, 41, 59)
            r2 = p.add_run()
            r2.text = "Lightweight, zero-configuration relational storage maintaining dataset metadata, column schemas, and raw observation records."
            r2.font.name = "Inter"
            r2.font.color.rgb = RGBColor(71, 85, 105)

    # Replace right-side diagram image on Slide 4
    if os.path.exists("slide4_arch.png"):
        s4.shapes.add_picture("slide4_arch.png", Inches(8.0), Inches(1.8), Inches(4.7), Inches(4.8))

    # -----------------------------------------------------------------
    # SLIDE 5: Results: Evaluation Metrics Matrix
    # -----------------------------------------------------------------
    s5 = prs.slides[4]
    for shape in s5.shapes:
        if shape.name == "TextBox 25":
            shape.text_frame.text = "Results: System Capabilities & Performance Matrix"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(30)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.has_table:
            table = shape.table
            headers = ["Analytical Component", "Underlying Technology", "Mathematical Metric", "Analytical Capability", "Execution Latency"]
            for col_idx, h in enumerate(headers):
                table.cell(0, col_idx).text = h
                table.cell(0, col_idx).text_frame.paragraphs[0].font.bold = True
                table.cell(0, col_idx).text_frame.paragraphs[0].font.name = "Poppins"
                table.cell(0, col_idx).text_frame.paragraphs[0].font.size = Pt(12)

            data_rows = [
                ["Pearson Linear Correlation", "SciPy / NumPy", "r = cov(X,Y)/(σx·σy)", "Linear co-variation & edge weighting", "< 12 ms (N=100)"],
                ["Spearman Rank Correlation", "SciPy Stats", "ρ = 1 - 6Σd²/n(n²-1)", "Non-parametric monotonic dependency", "< 15 ms (N=100)"],
                ["Hypothesis Testing (p-value)", "Student t-Distribution", "t = r·sqrt((n-2)/(1-r²))", "Filters spurious noise (p < 0.05)", "< 6 ms (N=100)"],
                ["OLS Linear Regression", "SciPy linregress", "y = β₁x + β₀ (R² score)", "Bivariate scatter slope & trendline", "< 8 ms (Pair)"]
            ]
            for row_idx, row_data in enumerate(data_rows):
                for col_idx, val in enumerate(row_data):
                    table.cell(row_idx + 1, col_idx).text = val
                    table.cell(row_idx + 1, col_idx).text_frame.paragraphs[0].font.name = "Inter"
                    table.cell(row_idx + 1, col_idx).text_frame.paragraphs[0].font.size = Pt(11)

    # -----------------------------------------------------------------
    # SLIDE 6: Results: Comparative Architecture Analysis
    # -----------------------------------------------------------------
    s6 = prs.slides[5]
    for shape in s6.shapes:
        if shape.name == "TextBox 6":
            shape.text_frame.text = "Results: Comparative Capability Analysis"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(30)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 4":
            shape.text_frame.text = "The full-stack architecture delivers a decisive capability transformation over the prototype: adding SQLite database persistence, arbitrary CSV ingestion, statistical significance p-value filtering, and sub-50ms API responsiveness."
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(13)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(71, 85, 105)

    if os.path.exists("slide6_comparative.png"):
        s6.shapes.add_picture("slide6_comparative.png", Inches(0.625), Inches(1.5), Inches(12.08), Inches(3.75))

    # -----------------------------------------------------------------
    # SLIDE 7: Results: Multi-Level Exploration Workflow
    # -----------------------------------------------------------------
    s7 = prs.slides[6]
    for shape in s7.shapes:
        if shape.name == "TextBox 6":
            shape.text_frame.text = "Results: Multi-Level Exploration Workflow"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(30)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 4":
            shape.text_frame.text = "Integrated analytical workflow: Analysts begin with macro network topology clustering, filter spurious edges via p-value thresholds, inspect bivariate scatter regressions with OLS fits, and isolate univariate histograms in sub-second cycles."
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(13)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(71, 85, 105)

    if os.path.exists("slide7_workflow.png"):
        s7.shapes.add_picture("slide7_workflow.png", Inches(0.625), Inches(1.5), Inches(12.08), Inches(4.35))

    # -----------------------------------------------------------------
    # SLIDE 8: Questions & Discussion
    # -----------------------------------------------------------------
    s8 = prs.slides[7]
    for shape in s8.shapes:
        if shape.name == "TextBox 3":
            shape.text_frame.text = "Questions & Discussion"
            shape.text_frame.paragraphs[0].font.name = "Poppins"
            shape.text_frame.paragraphs[0].font.size = Pt(64)
            shape.text_frame.paragraphs[0].font.bold = True
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(37, 99, 235)
        elif shape.name == "TextBox 4":
            shape.text_frame.text = "Thank you for your time."
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(20)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(30, 41, 59)
        elif shape.name == "TextBox 5":
            shape.text_frame.text = "Web Studio: http://127.0.0.1:8000"
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(12)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 116, 139)
        elif shape.name == "TextBox 6":
            shape.text_frame.text = "API Docs: http://127.0.0.1:8000/docs"
            shape.text_frame.paragraphs[0].font.name = "Inter"
            shape.text_frame.paragraphs[0].font.size = Pt(12)
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 116, 139)

    prs.save(out_ppt)
    print(f"Saved: {out_ppt}")

if __name__ == "__main__":
    build_presentation()
