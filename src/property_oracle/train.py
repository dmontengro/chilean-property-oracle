from pathlib import Path
import pandas as pd
from property_oracle.model import PropertyPricingModel
from property_oracle.logger import get_logger

logger = get_logger("training_job")

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw" / "market_data.csv"
MODEL_PATH = BASE_DIR / "models" / "price_predictor_v1.pkl"

def main():
    if not DATA_PATH.exists():
        logger.error(f"Dataset not found at {DATA_PATH}")
        return

    logger.info("Loading training data...")
    df = pd.read_csv(DATA_PATH)

    logger.info("Initializing model pipeline...")
    model = PropertyPricingModel()
    
    metrics = model.train(df)
    logger.info(f"Training completed. Metrics: R2={metrics['r2']:.4f}, MAE={metrics['mae']:.4f}")

    MODEL_PATH.parent.mkdir(exist_ok=True)
    model.save_model(MODEL_PATH)
    logger.info(f"Artifact serialized to {MODEL_PATH}")

if __name__ == "__main__":
    main()