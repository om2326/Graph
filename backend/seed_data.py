import numpy as np
from backend.database import insert_dataset, get_all_datasets

def generate_student_dataset():
    np.random.seed(42)
    N = 100
    subjects = ["Math", "Physics", "Chemistry", "Biology", "English", "History", "Economics", "ComputerScience"]
    
    quant = np.random.randn(N)
    verbal = np.random.randn(N)
    memory = np.random.randn(N)

    def make_col(lq, lv, lm, noise):
        raw = 70 + 12 * (lq * quant + lv * verbal + lm * memory + noise * np.random.randn(N))
        return np.clip(np.round(raw, 1), 35, 100)

    data = {
        "Math": make_col(1.0, 0.0, 0.1, 0.4),
        "Physics": make_col(0.9, 0.0, 0.1, 0.45),
        "Chemistry": make_col(0.7, 0.1, 0.3, 0.5),
        "ComputerScience": make_col(0.85, 0.1, 0.0, 0.45),
        "English": make_col(0.0, 1.0, 0.1, 0.45),
        "History": make_col(0.0, 0.75, 0.45, 0.5),
        "Economics": make_col(0.45, 0.5, 0.1, 0.55),
        "Biology": make_col(0.1, 0.25, 0.85, 0.5),
    }

    records = []
    for i in range(N):
        records.append({s: float(data[s][i]) for s in subjects})

    insert_dataset(
        dataset_id="student-performance",
        name="Student Academic Performance",
        description="Grades of 100 students across STEM and Humanities disciplines showing latent ability clustering.",
        columns=subjects,
        records=records,
        is_default=True
    )

def generate_economic_dataset():
    np.random.seed(101)
    N = 80
    cols = ["GDP_Growth", "Inflation_Rate", "Unemployment", "Interest_Rate", "Consumer_Confidence", "Stock_Index"]
    
    cycle = np.random.randn(N)
    supply_shock = np.random.randn(N)

    gdp = 2.5 + 1.8 * cycle - 0.5 * supply_shock + 0.4 * np.random.randn(N)
    unemp = 5.5 - 1.2 * cycle + 0.3 * supply_shock + 0.3 * np.random.randn(N)
    infl = 2.8 + 0.6 * cycle + 1.5 * supply_shock + 0.4 * np.random.randn(N)
    rates = 3.2 + 0.8 * infl - 0.4 * unemp + 0.3 * np.random.randn(N)
    conf = 100 + 15 * cycle - 10 * infl + 4 * np.random.randn(N)
    stocks = 4000 + 400 * cycle - 250 * rates + 80 * np.random.randn(N)

    records = []
    for i in range(N):
        records.append({
            "GDP_Growth": round(float(gdp[i]), 2),
            "Inflation_Rate": round(float(infl[i]), 2),
            "Unemployment": round(float(unemp[i]), 2),
            "Interest_Rate": round(float(rates[i]), 2),
            "Consumer_Confidence": round(float(conf[i]), 1),
            "Stock_Index": round(float(stocks[i]), 0)
        })

    insert_dataset(
        dataset_id="economic-indicators",
        name="Macroeconomic Indicators",
        description="Simulated economic indicators (GDP, Inflation, Interest Rates, Unemployment) displaying strong inverse and direct linkages.",
        columns=cols,
        records=records,
        is_default=True
    )

def seed_defaults_if_needed():
    existing = get_all_datasets()
    if not any(d["id"] == "student-performance" for d in existing):
        generate_student_dataset()
    if not any(d["id"] == "economic-indicators" for d in existing):
        generate_economic_dataset()
