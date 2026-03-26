# End-to-End Credit Card Fraud Detection System

## Project Overview
This project is a production-ready Machine Learning pipeline that predicts fraudulent credit card transactions. Built to handle extreme class imbalance (0.167%), it utilizes SMOTE, an XGBoost classifier, and a dual-tier architecture featuring a FastAPI backend and a Streamlit frontend.

**Kaggle Dataset Link:** [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

## Architecture
- **Model:** XGBoost Classifier (Selected via AUPRC evaluation)
- **Backend:** FastAPI (Running on Port 8007)
- **Frontend:** Streamlit

## Local Setup Instructions
1. Clone this repository to your local machine.
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt