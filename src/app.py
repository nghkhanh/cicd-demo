from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel
import pickle
import numpy as np


app = FastAPI(title="Iris Classification API", version="1.0.1")

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODEL_PATH = os.path.join(BASE_DIR, "models", "iris_model.pkl")
# print(f"model path: {MODEL_PATH}")
model = None

class PredictionInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictionOutput(BaseModel):
    prediction: int
    class_name: str
    confidence: float

def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("Model load successfully")

@app.on_event("startup")
async def startup_event():
    load_model()

@app.get("/")
async def root():
    return {
        "message": "Iris classification API",
        "status": "running",
        "endpoint": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_load": model is not None
    }

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    features = np.array([[
        input_data.sepal_length,
        input_data.sepal_width,
        input_data.petal_length,
        input_data.petal_width
    ]])

    predict = model.predict(features)[0]
    prob = model.predic_proba(features)[0]
    confidence = float(max(prob))

    class_names = ["setosa", "versicolor", "virginica"]

    return PredictionOutput(
        prediction=int(predict),
        class_name=class_names[predict],
        confidence=confidence
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
