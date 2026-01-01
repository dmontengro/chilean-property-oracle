# Chilean Property Oracle 🇨🇱 🏠

> **Automated Valuation Model (AVM)** for real estate in Santiago, Chile. 
> Designed to demonstrate end-to-end MLOps practices: from stochastic data generation to API deployment.

## 📌 Overview

This project implements a pricing engine that estimates rental values (in **UF** - *Unidad de Fomento*) based on geospatial features and property characteristics. 

Unlike traditional "toy projects" that rely on static datasets, this system utilizes a **Statistical Data Generator** powered by Copulas and multivariate distributions to simulate realistic market conditions, ensuring ethical compliance (GDPR-friendly) while preserving mathematical complexity.

## 🏗 Architecture

The solution follows a production-grade `src-layout` structure:

* **Core Logic:** Python 3.10+ package with type hinting.
* **API Layer:** High-performance REST API built with **FastAPI**.
* **Modeling:** Scikit-Learn pipelines wrapped in custom artifacts.
* **Quality Assurance:** Automated linting (`Ruff`) and testing (`Pytest`).
* **Deployment:** Dockerized application ready for cloud orchestration.

## 🚀 Quick Start

### Prerequisites
* Python 3.10+
* Docker (Optional)

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/dmontengro/chilean-property-oracle.git](https://github.com/dmontengro/chilean-property-oracle.git)
   cd chilean-property-oracle

2. Create a virtual environment and install dependencies:
   ```bash
    # Create virtual env
    python -m venv .venv

    # Activate it (Windows)
    .venv\Scripts\activate

    # Install dependencies
    pip install -e .[dev]

3. Run the tests to ensure integrity:
   ```bash
    pytest

## 🛠 Tech Stack

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **Language** | Python 3.10 | Strong typing support and pattern matching. |
| **Backend** | FastAPI | Asynchronous capabilities and auto-generated Swagger docs. |
| **ML Engine** | Scikit-Learn | Robustness for tabular data regression tasks. |
| **Linting** | Ruff | Extremely fast static analysis (Rust-based). |
| **Container** | Docker | Ensures reproducibility across environments. |