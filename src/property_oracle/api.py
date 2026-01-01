from contextlib import asynccontextmanager
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from property_oracle.schemas import PropertyInput, PredictionOutput
from property_oracle.logger import get_logger

logger = get_logger("api")
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load artifacts on startup
    base_dir = Path(__file__).resolve().parents[2]
    model_path = base_dir / "models" / "price_predictor_v1.pkl"
    
    if model_path.exists():
        logger.info(f"Loading model from {model_path}")
        ml_models["predictor"] = joblib.load(model_path)
    else:
        logger.warning(f"Model artifact not found at {model_path}")
    
    yield
    ml_models.clear()

app = FastAPI(title="Property Valuation Service", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": "predictor" in ml_models}

@app.post("/predict", response_model=PredictionOutput)
def predict(payload: PropertyInput):
    if "predictor" not in ml_models:
        raise HTTPException(status_code=503, detail="Model service unavailable")
    
    try:
        input_df = pd.DataFrame([payload.model_dump()])
        prediction = ml_models["predictor"].predict(input_df)[0]
        
        # 2.21 is the documented MAE from training validation
        MAE = 2.21
        
        return {
            "estimated_price_uf": round(prediction, 2),
            "confidence_interval_lower": round(prediction - MAE, 2),
            "confidence_interval_upper": round(prediction + MAE, 2),
            "currency": "UF"
        }
        
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal processing error")