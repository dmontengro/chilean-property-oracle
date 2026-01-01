from pydantic import BaseModel, Field, PositiveFloat
from typing import Literal

# Actualizamos el contrato con las nuevas comunas
ValidComuna = Literal[
    'Vitacura', 'Las Condes', 'Lo Barnechea', 'Providencia', 
    'Ñuñoa', 'Santiago', 'San Miguel', 
    'Macul', 'La Florida', 'Maipú', 'Estación Central'
]
class PropertyInput(BaseModel):
    """Modelo de entrada: Lo que el usuario debe enviar"""
    comuna: ValidComuna = Field(..., description="Comuna del departamento", example="Providencia")
    surface_m2: PositiveFloat = Field(..., description="Superficie total en m2", example=55.0)
    distance_to_metro: PositiveFloat = Field(..., description="Distancia al metro más cercano en metros", example=350.0)

class PredictionOutput(BaseModel):
    """Modelo de salida: Lo que nuestra API responderá"""
    estimated_price_uf: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    currency: str = "UF"