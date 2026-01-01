# Property Valuation Engine (Chile Market)

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

## Abstract

A stochastic pricing engine designed to estimate residential rental values in Santiago, Chile. This project implements an end-to-end MLOps pipeline, featuring synthetic data generation based on Q4 2025 market heuristics, gradient boosting regression, and a REST API for inference.

The system is engineered to demonstrate production-grade software practices in a Data Science context, utilizing a strict `src-layout`, type hinting, and automated validation.

## Key Features

* **Synthetic Data Generation:** Implements a custom generator using domain-specific coefficients to simulate non-linear market behaviors (e.g., inverse distance weighting for metro proximity).
* **Robust Modeling:** Utilizes Scikit-Learn pipelines to encapsulate preprocessing (OneHotEncoding, Scaling) and model inference (Gradient Boosting Regressor) into a single serializable artifact.
* **API Layer:** High-performance REST API built with **FastAPI**, featuring Pydantic data validation and structured JSON logging.
* **Reproducibility:** Deterministic seeding for data generation and model training ensures consistent results across environments.

## Architecture

The solution follows a modular architecture:

1.  **Data Ingestion:** `data_gen.py` produces a synthetic dataset calibrated against real market listings (PortalInmobiliario/Toctoc heuristics).
2.  **Training Pipeline:** `train.py` executes the ETL process, trains the regressor, and serializes the pipeline to `.pkl`.
3.  **Inference Service:** `api.py` loads the artifact into memory and serves predictions via HTTP endpoints.

## Installation

### Prerequisites
* Python 3.10 or higher

### Setup

1.  Clone the repository:
    ```bash
    git clone [https://github.com/dmontengro/chilean-property-oracle.git](https://github.com/dmontengro/chilean-property-oracle.git)
    cd chilean-property-oracle
    ```

2.  Create and activate the virtual environment:
    ```bash
    # Unix/MacOS
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  Install dependencies in editable mode:
    ```bash
    pip install -e .[dev]
    ```

## Usage

### 1. Data Generation
Generates the synthetic dataset based on configured market heuristics.
```bash
python src/property_oracle/data_gen.py
```
### 2. Model Training
Trains the Gradient Boosting model and saves the artifact to models/.

```bash
python -m src.property_oracle.train
```

### 3. API Deployment
Launches the inference server locally.
```bash
uvicorn src.property_oracle.api:app --reload
```
Access the interactive documentation at http://127.0.0.1:8000/docs.

## Project Structure
```Plaintext
chilean-property-oracle/
├── data/                   # Generated datasets
├── models/                 # Serialized model artifacts (.pkl)
├── notebooks/              # Exploratory Data Analysis (EDA)
├── src/
│   └── property_oracle/
│       ├── api.py          # FastAPI application
│       ├── config.py       # Configuration settings
│       ├── data_gen.py     # Synthetic data generator
│       ├── logger.py       # Logging configuration
│       ├── model.py        # ML Pipeline definition
│       ├── schemas.py      # Pydantic data models
│       └── train.py        # Training script
├── tests/                  # Unit and integration tests
├── pyproject.toml          # Dependency and project management
└── README.md               # Project documentation
```
## Tech Stack

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **Runtime** | Python 3.10 | Type hinting and pattern matching support.. |
| **Web Framework** | FastAPI | Async support and automatic OpenAPI generation. |
| **ML Core** | Scikit-Learn | Robust implementation of Gradient Boosting.. |
| **Data Processing** | Pandas/ NumPy | Vectorized operations for efficient data manipulation. |
| **Linting** | Ruff | High-performance static analysis. |

## License
This project is licensed under the MIT License.

Disclaimer: *This software generates synthetic data for demonstration purposes based on market approximations. It should not be used for actual financial valuation.*