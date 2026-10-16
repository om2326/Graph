import os
import io
import uuid
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import (
    init_db,
    get_all_datasets,
    get_dataset,
    get_dataset_records,
    insert_dataset,
    delete_dataset
)
from backend.seed_data import seed_defaults_if_needed
from backend.stats import compute_correlations, get_scatter_data, get_column_distribution

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_defaults_if_needed()
    yield

app = FastAPI(title="Correlation Network Studio API", version="1.0.0", lifespan=lifespan)

# Enable CORS for local development flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Graph Visualization API is running."}

@app.get("/api/datasets")
def list_datasets():
    return get_all_datasets()

@app.get("/api/datasets/{dataset_id}")
def read_dataset(dataset_id: str):
    ds = get_dataset(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return ds

@app.post("/api/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form("")
):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")

    # Select only numeric columns
    numeric_df = df.select_dtypes(include=["number"]).dropna()
    if numeric_df.shape[1] < 2:
        raise HTTPException(
            status_code=400, 
            detail=f"Dataset must contain at least 2 numeric columns for correlation analysis. Found {numeric_df.shape[1]}."
        )
    if len(numeric_df) < 3:
        raise HTTPException(status_code=400, detail="Dataset must have at least 3 valid data rows.")

    dataset_id = f"custom-{uuid.uuid4().hex[:8]}"
    cols = list(numeric_df.columns)
    records = numeric_df.to_dict(orient="records")

    insert_dataset(
        dataset_id=dataset_id,
        name=name.strip() or file.filename,
        description=description.strip() or f"Uploaded CSV containing {len(records)} rows and {len(cols)} numeric variables.",
        columns=cols,
        records=records,
        is_default=False
    )

    return get_dataset(dataset_id)

@app.delete("/api/datasets/{dataset_id}")
def remove_dataset(dataset_id: str):
    success = delete_dataset(dataset_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete default presets or dataset was not found.")
    return {"message": "Dataset deleted successfully", "id": dataset_id}

@app.get("/api/datasets/{dataset_id}/correlations")
def get_correlations(
    dataset_id: str,
    method: str = Query("pearson", pattern="^(pearson|spearman)$"),
    min_threshold: float = Query(0.0, ge=0.0, le=1.0),
    max_p_value: float = Query(1.0, ge=0.0, le=1.0)
):
    ds = get_dataset(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    records = get_dataset_records(dataset_id)
    result = compute_correlations(
        records=records,
        columns=ds["columns"],
        method=method,
        min_threshold=min_threshold,
        max_p_value=max_p_value
    )
    result["dataset"] = ds
    return result

@app.get("/api/datasets/{dataset_id}/scatter")
def get_scatter(
    dataset_id: str,
    x: str = Query(...),
    y: str = Query(...)
):
    ds = get_dataset(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if x not in ds["columns"] or y not in ds["columns"]:
        raise HTTPException(status_code=400, detail=f"Columns '{x}' and '{y}' must be valid numeric columns in the dataset.")
    
    records = get_dataset_records(dataset_id)
    return get_scatter_data(records, x, y)

@app.get("/api/datasets/{dataset_id}/distribution")
def get_distribution(
    dataset_id: str,
    column: str = Query(...),
    bins: int = Query(12, ge=4, le=50)
):
    ds = get_dataset(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if column not in ds["columns"]:
        raise HTTPException(status_code=400, detail=f"Column '{column}' is not in the dataset.")
    
    records = get_dataset_records(dataset_id)
    bin_count = int(bins.default) if hasattr(bins, "default") else int(bins)
    return get_column_distribution(records, column, num_bins=bin_count)

# Mount frontend files
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    @app.get("/presentation")
    def serve_presentation():
        return FileResponse(os.path.join(FRONTEND_DIR, "presentation.html"))
