# StudentIQ — Student Retention & Welfare Intelligence

> An end-to-end data analytics and AI platform that transforms messy student records into actionable retention and welfare insights.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)](https://fastapi.tiangolo.com/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-orange.svg)](https://duckdb.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg)](https://scikit-learn.org/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Live Demo

### 🌐 Streamlit Dashboard

👉 **[Open StudentIQ Live Dashboard](https://studentiq-retention-welfare-r6.streamlit.app/)**

### 💻 GitHub Repository

👉 **[View Source Code](https://github.com/rajatrawat-dev/StudentIQ-Retention-Welfare)**

---

## 📌 Overview

**StudentIQ** is an end-to-end student retention and welfare analytics platform built to transform messy and fragmented student records into reliable analytical insights.

The platform combines data engineering, analytics, machine learning, visualization, REST APIs, and natural-language querying into a single decision-support system.

### Core Pipeline

```text
Raw Student Data
       ↓
Data Cleaning & Validation
       ↓
Data Quality Assessment
       ↓
DuckDB Analytical Layer
       ↓
Analytics & KPIs
       ↓
Retention Risk Analysis
       ↓
Machine Learning
       ↓
AI Analyst
       ↓
Interactive Streamlit Dashboard
🎯 Problem Statement

Educational institutions often maintain student information across fragmented datasets.

Common problems include:

Missing values
Duplicate records
Inconsistent student IDs
Different department naming conventions
Multiple attendance formats
Invalid academic values
Inconsistent dates
Data-quality issues

These problems make it difficult to obtain reliable insights and identify students who may require additional academic support.

StudentIQ addresses this by creating a reproducible data-rescue, analytics, and decision-support pipeline.

✨ Key Features
1. Data Rescue Engine

StudentIQ includes an automated data-cleaning pipeline capable of handling:

Tolerant data ingestion
Column-name normalization
Duplicate detection
Student ID normalization
Name normalization
Department standardization
Gender normalization
Attendance normalization
CGPA validation
Date normalization
Missing-value imputation
Academic anomaly detection
Derived risk features
Data-quality scoring
2. Data Quality Monitoring

Instead of silently modifying problematic records, StudentIQ provides visibility into data quality.

The system tracks:

Missing values
Duplicate records
Invalid values
Normalization operations
Detected anomalies
Overall data-quality score
3. DuckDB Analytical Engine

StudentIQ uses DuckDB as an embedded analytical database.

The analytical layer supports:

Institutional KPIs
Department-level analysis
Student-level exploration
Risk distribution
Cohort comparisons
Analytical SQL queries

DuckDB provides a lightweight analytical layer without requiring a separate database server.

4. Retention Risk Analysis

The platform combines academic indicators to calculate a continuous retention-risk indicator.

Risk categories:

LOW
MEDIUM
HIGH
CRITICAL

The system can prioritize students who may require additional academic support.

Risk scores are analytical indicators and should not be treated as medical, psychological, or clinical diagnoses.

🤖 AI Analyst

StudentIQ includes a natural-language analytical interface that allows users to ask questions about the dataset.

Example
Which departments have the lowest average CGPA?

The system can:

Natural Language Question
          ↓
Intent Detection
          ↓
Safe SQL Generation
          ↓
DuckDB Query
          ↓
Result Analysis
          ↓
Chart Selection
          ↓
Insight
🔐 SQL Safety

The AI Analyst uses a read-only analytical approach.

Potentially destructive SQL operations are blocked, including:

DROP
DELETE
UPDATE
INSERT
ALTER
TRUNCATE
PRAGMA

Multi-statement SQL injection attempts are also rejected.

The goal is to ensure that the analytical assistant cannot modify the underlying analytical database through user queries.

📊 Automatic Visualization

The AI Analyst selects visualizations based on the type of analytical question.

Analytical Intent	Chart
Category comparison	Bar Chart
Relationship between variables	Scatter Plot
Proportion / distribution	Donut Chart
Ranking	Horizontal Bar Chart
Trend analysis	Line Chart

This allows users to receive both the analytical result and an appropriate visual representation.

🧠 Machine Learning

StudentIQ includes a Scikit-Learn machine-learning pipeline.

Model
Random Forest Classifier

The ML pipeline includes:

Feature preparation
Model training
Prediction
Dataset-size validation
Model evaluation
Rule-based fallback

If the dataset is too small for reliable statistical evaluation, the application can fall back to deterministic analytical rules.

🖥️ Dashboard

The Streamlit application provides five main areas:

1. Executive Dashboard

Provides high-level institutional KPIs and important insights.

2. Data Quality

Displays data-quality metrics, anomalies, and cleaning results.

3. Student Analytics

Allows exploration of student and department-level information.

4. Retention Risk

Provides risk distribution and support-priority analysis.

5. AI Analyst

Allows users to ask analytical questions in natural language.

🏗️ System Architecture
                         ┌───────────────────┐
                         │   Raw Data Files  │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Data Rescue Layer │
                         │                   │
                         │ Cleaning          │
                         │ Normalization     │
                         │ Validation        │
                         │ Deduplication     │
                         │ Imputation        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Cleaned Dataset   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │      DuckDB       │
                         │ Analytical Layer  │
                         └─────────┬─────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
                  ▼                ▼                ▼
          ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
          │  Analytics   │ │ ML Risk      │ │ AI Analyst   │
          │  & KPIs      │ │ Prediction   │ │              │
          └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                 │                │                │
                 └────────────────┼────────────────┘
                                  ▼
                       ┌─────────────────────┐
                       │ Streamlit Dashboard │
                       └─────────────────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │ Decision Support   │
                       └─────────────────────┘
📂 Project Structure
StudentIQ-Retention-Welfare/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .env.example
├── .gitignore
│
├── app/
│   ├── __init__.py
│   ├── streamlit_app.py
│   │
│   ├── components/
│   │   ├── sidebar.py
│   │   ├── kpi_cards.py
│   │   ├── charts.py
│   │   ├── tables.py
│   │   └── agent_chat.py
│   │
│   └── pages/
│       ├── 01_Executive_Dashboard.py
│       ├── 02_Data_Quality.py
│       ├── 03_Student_Analytics.py
│       ├── 04_Risk_Analysis.py
│       └── 05_AI_Analyst.py
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   └── routes/
│       ├── __init__.py
│       ├── students.py
│       ├── analytics.py
│       └── agent.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── demo_questions.md
│
├── notebooks/
│   └── exploration.ipynb
│
├── scripts/
│   ├── generate_messy_data.py
│   ├── clean_data.py
│   ├── build_database.py
│   └── train_model.py
│
├── src/
│   ├── config/
│   ├── data/
│   ├── analytics/
│   ├── ml/
│   ├── agent/
│   └── utils/
│
└── tests/
    ├── test_cleaner.py
    ├── test_validator.py
    ├── test_metrics.py
    ├── test_queries.py
    └── test_agent.py
⚙️ Installation
Prerequisites
Python 3.11+
Git
pip
Optional: Ollama for local LLM functionality
1. Clone the Repository
git clone https://github.com/rajatrawat-dev/StudentIQ-Retention-Welfare.git
cd StudentIQ-Retention-Welfare
2. Create a Virtual Environment
Windows PowerShell
python -m venv .venv

Activate it:

.\.venv\Scripts\Activate.ps1

If PowerShell blocks activation:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then:

.\.venv\Scripts\Activate.ps1
3. Install Dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
🔄 Run the Data Pipeline

Execute the pipeline in order.

Step 1 — Generate / Prepare Data
python scripts/generate_messy_data.py
Step 2 — Clean Data
python scripts/clean_data.py
Step 3 — Build DuckDB Database
python scripts/build_database.py
Step 4 — Train Risk Model
python scripts/train_model.py
🧪 Run Tests

Run all tests:

pytest -v

Or:

python -m pytest -q
🚀 Run Streamlit Locally

Start the dashboard from the project root:

streamlit run app/streamlit_app.py

Then open:

http://localhost:8501
🔌 Run FastAPI

Start the backend:

uvicorn api.main:app --reload

API:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs
🤖 Optional Ollama Setup

Ollama can be used for local LLM inference.

After installing Ollama:

ollama --version

Download a lightweight model:

ollama pull llama3.2:3b

Run the model:

ollama run llama3.2:3b

The application can fall back to its deterministic rule-based analytical engine if Ollama is unavailable.

☁️ Deployment — Streamlit Community Cloud

The application is deployed using Streamlit Community Cloud.

Repository
rajatrawat-dev/StudentIQ-Retention-Welfare
Branch
main
Main Streamlit File
app/streamlit_app.py
Live Application
https://studentiq-retention-welfare-r6.streamlit.app/
🔁 Update the Hosted Application

Whenever changes are made locally:

cd "C:\Users\VICTUS\StudentIQ-Retention-Welfare"

Check changes:

git status

Add changes:

git add .

Commit:

git commit -m "Update StudentIQ dashboard"

Push to GitHub:

git push origin main

Streamlit Community Cloud will automatically rebuild the application after the GitHub update.

💬 Example Analytical Questions

The AI Analyst can be tested with questions such as:

Show students with attendance below 60%.
Which departments have the lowest average CGPA?
Compare CSE, ECE and IT.
Show the relationship between attendance and CGPA.
Which students are at high risk?
Show the distribution of student risk.
Which department needs the most academic support?
Show the top 10 students by CGPA.
🛠️ Technology Stack
Layer	Technology
Programming	Python 3.11+
Data Processing	Pandas, NumPy
Analytical Database	DuckDB
Machine Learning	Scikit-Learn
Visualization	Plotly
Dashboard	Streamlit
Backend API	FastAPI
API Server	Uvicorn
Data Validation	Pydantic
Testing	Pytest
Local LLM	Ollama
Version Control	Git + GitHub
🔒 Responsible Use

StudentIQ is designed as a decision-support and analytics platform.

Retention-risk scores are indicators that can help identify records requiring further review.

They should not be treated as definitive judgments about a student's future performance or circumstances.

Human review should remain part of any real-world academic intervention.

🔮 Future Improvements

Potential improvements include:

Longitudinal student tracking
Explainable AI using SHAP
Advanced cohort analysis
Learning Management System integration
Automated notifications
Additional institutional data sources
Role-based access control
More advanced agentic analytics
Improved model explainability
👨‍💻 Author
Rajat Rawat

GitHub:
https://github.com/rajatrawat-dev

Project Repository:
https://github.com/rajatrawat-dev/StudentIQ-Retention-Welfare

Live Dashboard:
https://studentiq-retention-welfare-r6.streamlit.app/

📄 License

This project is licensed under the MIT License.

See the LICENSE file for details.


### Then push the README

After replacing the README, open PowerShell:

```powershell
cd "C:\Users\VICTUS\StudentIQ-Retention-Welfare"

Run:

git add README.md
git commit -m "Improve README and add live demo"
git push origin main

