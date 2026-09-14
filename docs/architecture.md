# StudentIQ Architectural Blueprint

StudentIQ is architected around a multi-stage **Data Rescue to Agentic Insights** pipeline designed for academic retention and welfare intelligence.

## System Architecture

```mermaid
flowchart TD
    subgraph DataRescue[Layer 1: Data Rescue Engine]
        A[Raw Messy CSV] --> B[Normalizers: ID, Name, Dept, Gender, Att, CGPA, Dates]
        B --> C[Deduplication & Collision Resolution]
        C --> D[Department-Median Missing Imputation]
        D --> E[Academic Anomaly Detection]
        E --> F[Canonical Validated Dataset]
        E --> G[Data Quality Report JSON]
    end

    subgraph AnalyticalStore[Layer 2: Analytical Store & ML]
        F --> H[(Embedded DuckDB Engine)]
        H --> I[Analytical Views: department_summary, risk_summary]
        F --> J[Scikit-Learn Random Forest Pipeline]
        J --> K[Persisted Joblib Model & Calibration Fallback]
    end

    subgraph IntelligenceLayer[Layer 3: Agentic AI Analyst]
        L[User Natural Language Query] --> M[Intent Detection Engine]
        M --> N[Query Generator: Local Ollama LLM / Rule Engine]
        N --> O{AI Safety Validator}
        O -- "Unsafe Keywords / Multi-stmt" --> P[Query Rejection & Security Alert]
        O -- "Approved SELECT" --> Q[DuckDB Analytical Execution]
        Q --> R[Chart Recommendation Engine]
        Q --> S[Natural Language Synthesis]
    end

    subgraph Presentation[Layer 4: Presentation & API]
        T[Streamlit Multi-Page Analytics Dashboard]
        U[FastAPI High-Performance REST Endpoints]
        H --> T
        H --> U
        K --> T
        K --> U
        R --> T
        S --> T
    end
```

## Layer Descriptions

1. **Data Rescue Engine**: Converts malformed, inconsistent student data into canonical records with verifiable data quality scores.
2. **DuckDB Analytics**: Columnar OLAP database providing fast aggregations across cohorts, departments, and grade bands.
3. **ML Risk Model**: Scikit-learn classification pipeline assessing retention vulnerability into 4 calibrated tiers (LOW, MEDIUM, HIGH, CRITICAL).
4. **Agentic Copilot**: Natural language query interface with strict AST/regex query sanitization preventing SQL injection or state mutation.
5. **Presentation**: Polished Streamlit UI with dark glassmorphic styling and FastAPI backend endpoints.