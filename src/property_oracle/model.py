import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error

class PropertyPricingModel:
    def __init__(self):
        # Definimos el Pipeline de Preprocesamiento
        # 1. Variables Numéricas: Se estandarizan (Mean=0, Std=1)
        numeric_features = ['surface_m2', 'distance_to_metro']
        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])

        # 2. Variables Categóricas (Comuna): One-Hot Encoding
        categorical_features = ['comuna']
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # 3. Unimos todo en un Preprocessor
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        # 4. Definimos el Modelo Final (Gradient Boosting es robusto y potente)
        self.pipeline = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('regressor', GradientBoostingRegressor(n_estimators=200, random_state=42))
        ])

    def train(self, data: pd.DataFrame):
        """Entrena el modelo completo (preproceso + regresión)"""
        X = data.drop('price_uf', axis=1)
        y = data['price_uf']

        # Split clásico 80/20
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        print("🧠 Entrenando Gradient Boosting...")
        self.pipeline.fit(X_train, y_train)

        # Evaluación
        y_pred = self.pipeline.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"✅ Modelo Entrenado.")
        print(f"   R² Score: {r2:.4f} (¡Mientras más cerca de 1.0 mejor!)")
        print(f"   MAE: {mae:.2f} UF (Error promedio en predicción)")
        
        return {"r2": r2, "mae": mae}

    def predict(self, new_data: pd.DataFrame) -> list[float]:
        """Hace predicciones sobre datos nuevos"""
        return self.pipeline.predict(new_data).tolist()

    def save_model(self, filepath: Path):
        """Guarda el pipeline completo como archivo .pkl"""
        joblib.dump(self.pipeline, filepath)
        print(f"💾 Modelo guardado en: {filepath}")