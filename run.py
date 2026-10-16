import uvicorn
import os

if __name__ == "__main__":
    print("================================================================")
    print(" Starting Correlation Network Studio (Full-Stack)")
    print(" Frontend & API running at: http://127.0.0.1:8000")
    print(" API Documentation at:      http://127.0.0.1:8000/docs")
    print("================================================================")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
