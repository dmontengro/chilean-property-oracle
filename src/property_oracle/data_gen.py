import numpy as np
import pandas as pd
from pathlib import Path
from property_oracle.logger import get_logger

logger = get_logger(__name__)

# Market coefficients based on Q4 2025 analysis (PortalInmobiliario/Toctoc)
COMUNA_MARKET_PROFILE = {
    'Vitacura':       {'base': 3.5, 'm2_val': 0.32}, 
    'Las Condes':     {'base': 2.5, 'm2_val': 0.30},
    'Lo Barnechea':   {'base': 3.0, 'm2_val': 0.29},
    'Providencia':    {'base': 2.0, 'm2_val': 0.28},
    'Ñuñoa':          {'base': 2.0, 'm2_val': 0.24},
    'San Miguel':     {'base': 1.5, 'm2_val': 0.17},
    'Macul':          {'base': 1.5, 'm2_val': 0.17},
    'Santiago':       {'base': 1.2, 'm2_val': 0.18}, 
    'La Florida':     {'base': 1.2, 'm2_val': 0.15},
    'Maipú':          {'base': 1.0, 'm2_val': 0.14},
    'Estación Central': {'base': 0.8, 'm2_val': 0.14}
}

COMMUNES = list(COMUNA_MARKET_PROFILE.keys())
PROBABILITIES = [0.05, 0.10, 0.05, 0.10, 0.10, 0.20, 0.10, 0.05, 0.10, 0.10, 0.05]

def generate_market_data(n_samples: int = 5000) -> pd.DataFrame:
    """
    Simulates real estate market data using calibrated heuristics.
    Target: Monthly rent in UF.
    """
    np.random.seed(42)
    
    # 1. Feature Generation
    selected_comunas = np.random.choice(COMMUNES, size=n_samples, p=PROBABILITIES)
    
    # Log-normal distribution for surface area to handle skewness
    surfaces = np.random.lognormal(mean=3.8, sigma=0.4, size=n_samples).astype(int)
    surfaces = np.clip(surfaces, 20, 300)
    
    dist_metro = np.random.exponential(scale=800, size=n_samples).astype(int)
    
    # 2. Price Calculation (Ground Truth)
    prices = []
    
    for i in range(n_samples):
        comuna = selected_comunas[i]
        params = COMUNA_MARKET_PROFILE[comuna]
        
        # Location logic: diminishing returns on metro proximity
        # Max impact ~3.0 UF at 0m, decaying to ~1.0 UF at 1km
        metro_impact = 3000 / (dist_metro[i] + 500)
        
        # Market noise (idiosyncratic risk)
        noise = np.random.normal(0, 1.5)
        
        price = params['base'] + (surfaces[i] * params['m2_val']) + metro_impact + noise
        prices.append(max(5.0, round(price, 2)))

    return pd.DataFrame({
        'comuna': selected_comunas,
        'surface_m2': surfaces,
        'distance_to_metro': dist_metro,
        'price_uf': prices
    })

if __name__ == "__main__":
    ROOT_DIR = Path(__file__).resolve().parents[2]
    DATA_PATH = ROOT_DIR / "data" / "raw" / "market_data.csv"
    
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Generating {5000} samples based on V4 calibration...")
    df = generate_market_data(5000)
    
    df.to_csv(DATA_PATH, index=False)
    logger.info(f"Dataset saved to {DATA_PATH}")