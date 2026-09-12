# 🎓 Student Retention & Welfare Efficacy Tracker

> **From Messy Student Data to Actionable Retention & Welfare Insights**

## 📌 Overview

The **Student Retention & Welfare Efficacy Tracker** is a data-driven analytics platform designed to help educational institutions identify students who may be at risk of disengagement or dropout and evaluate the effectiveness of academic and welfare interventions.

The system transforms messy and inconsistent student data into clean, structured, analytics-ready information and converts it into actionable insights through data analytics, machine learning, interactive visualizations, and an AI-powered analytical assistant.

Instead of relying mainly on reactive identification of struggling students, the platform aims to provide **early, data-driven indicators** that can help faculty, administrators, and student-support teams take appropriate action.

---

## 🎯 Problem

Educational institutions collect student information from multiple academic, attendance, engagement, and welfare-related sources.

However, this data can contain:

- Duplicate student records
- Missing values
- Inconsistent student IDs
- Different department naming conventions
- Inconsistent attendance formats
- Incorrect data types
- Inconsistent categorical values
- Incomplete academic information
- Broken relationships between datasets

These problems make it difficult to obtain a reliable picture of student retention and welfare.

Without a unified analytical system, institutions may struggle to answer:

- Which students are at higher risk of dropping out?
- Which departments have lower retention?
- Is attendance associated with retention?
- Which students require additional support?
- Are welfare interventions improving student outcomes?
- Which intervention programs are most effective?
- Where should institutional resources be prioritized?

The project aims to move from **reactive student support to proactive, data-driven decision-making**.

---

## 💡 Proposed Solution

Our platform follows an end-to-end approach:

**Messy Data → Data Rescue → Data Validation → Analytics → Risk Analysis → Dashboard → AI Insights**

The system first processes messy student data to detect duplicates, missing values, inconsistent formats, invalid records, and broken relationships.

The cleaned data is then transformed into a structured analytical model.

Analytics and SQL queries are used to calculate retention, attendance, academic performance, risk, and welfare-related metrics.

The resulting insights are presented through an interactive dashboard designed for educational decision-makers.

An AI Analyst provides an optional natural-language interface through which users can ask analytical questions and receive appropriate results and visualizations.

---

## 🧹 Data Rescue & Data Quality

Data rescue is one of the core components of the platform.

The pipeline is designed to identify and resolve common problems found in messy enterprise-style student datasets.

### Data Cleaning Operations

- Duplicate record detection
- Student ID normalization
- Missing-value detection
- Invalid-value detection
- Data-type correction
- Department normalization
- Category standardization
- Attendance normalization
- Date standardization
- Outlier detection
- Relationship validation
- Data-quality reporting

### Example

Raw student data may contain:

Student_ID    Department       Attendance    CGPA
---------------------------------------------------
101           CSE              85%            8.2
101           cse              85             8.20
102           Computer Sci     0.78           7.5

The data-rescue pipeline converts inconsistent representations into a standardized analytical format:

Student_ID    Department    Attendance    CGPA
------------------------------------------------
101           CSE           0.85          8.20
102           CSE           0.78          7.50

The pipeline maintains a clear separation between:

Raw Data → Cleaned Data → Analytics Data

This improves reproducibility, transparency, and data quality.

📊 Analytics Layer

The analytics layer converts cleaned student information into meaningful institutional metrics.

Key Metrics
Total Students
Retained Students
Retention Rate
At-Risk Students
Average CGPA
Average Attendance
Academic Risk
Attendance Risk
Welfare Support Coverage
Intervention Success Rate
Department-wise Retention
Semester-wise Retention
Academic Performance Distribution
Retention Analysis

The system can analyze retention patterns across:

Departments
Semesters
Academic performance levels
Attendance groups
Student-risk categories
Welfare intervention groups

This enables decision-makers to identify areas requiring additional attention.

🚨 Student Risk Analysis

The platform provides analytical indicators for students who may require additional academic or welfare support.

Potential risk indicators include:

Low attendance
Low CGPA
Increasing academic difficulties
Backlogs
Previous intervention history
Welfare-support requirements
Engagement indicators
Historical retention patterns

Students can be grouped into analytical risk categories:

LOW RISK
Stable academic and engagement indicators

MEDIUM RISK
One or more warning indicators

HIGH RISK
Multiple indicators requiring closer attention

Risk scores are intended to support human decision-making and should not be treated as automatic judgments about a student.

🧠 AI & Machine Learning

Machine-learning techniques can be used to identify patterns associated with student retention and academic risk.

Possible approaches include:

Classification
Risk scoring
Student segmentation
Feature analysis
Retention prediction

The system evaluates models using actual validation results from the available dataset.

No artificial or hardcoded model accuracy is used.

The final model and evaluation metrics depend on the dataset and experiments performed during implementation.

🤖 AI Analyst

The optional AI Analyst allows users to interact with the analytics system using natural language.

Example questions include:

Show students with attendance below 60%.
Compare retention rates across departments.
Which department has the highest number of at-risk students?
Show the relationship between attendance and CGPA.
Which welfare intervention has the best outcome?
AI Agent Workflow
User Question
      ↓
Intent Detection
      ↓
Schema Identification
      ↓
SQL Generation
      ↓
SQL Validation
      ↓
Query Execution
      ↓
Result Analysis
      ↓
Chart Selection
      ↓
Visualization
      ↓
Natural-Language Explanation

The AI Analyst operates on the structured analytics layer rather than directly manipulating raw student data.

📈 Executive Dashboard

The platform provides an interactive dashboard for monitoring student retention and welfare indicators.

Dashboard Components
Student population overview
Retention rate
At-risk student count
Average CGPA
Average attendance
Department-wise retention
Risk distribution
Academic performance
Welfare intervention analysis
Semester trends
Student-level analytical tables
Interactive filters
AI Analyst

The dashboard is designed to help administrators move from high-level institutional metrics to detailed student-level analysis.

📊 Visualization

Different visualization techniques are selected according to the analytical requirement.

Analytical Purpose	Visualization
Department comparison	Bar Chart
Retention trend	Line Chart
Risk distribution	Donut Chart
CGPA distribution	Histogram
Attendance vs CGPA	Scatter Plot
Student ranking	Horizontal Bar Chart
Important metric	KPI Card

The goal is to make complex student data easier to understand and turn analytics into actionable insights.

🔄 System Workflow
                    MESSY STUDENT DATA
                            │
                            ▼
                 ┌─────────────────────┐
                 │     DATA RESCUE     │
                 │ Cleaning & Validation│
                 └──────────┬──────────┘
                            │
                            ▼
                    CLEAN STUDENT DATA
                            │
                            ▼
                 ┌─────────────────────┐
                 │   ANALYTICS LAYER   │
                 │   Python + SQL      │
                 │      DuckDB         │
                 └──────────┬──────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        RETENTION ANALYSIS        RISK ANALYSIS
                │                       │
                └───────────┬───────────┘
                            │
                            ▼
                  EXECUTIVE DASHBOARD
                            │
                            ▼
                      AI ANALYST
                            │
                            ▼
                   ACTIONABLE INSIGHTS
                            │
                            ▼
                  STUDENT SUPPORT
🌟 Key Features
🧹 Automated student-data cleaning
🔍 Duplicate detection
✅ Data validation
📋 Data-quality reporting
📊 Retention analytics
🎓 Academic performance analysis
🚨 Student risk analysis
🤝 Welfare intervention analysis
📈 Interactive executive dashboard
🔎 Department and semester filtering
🤖 Natural-language AI Analyst
🗃️ SQL-based analytics
🔄 Reproducible data pipeline
🧪 Automated testing
📊 Dynamic visualization
🎯 Welfare Efficacy Analysis

The system is designed not only to identify students requiring support, but also to examine whether interventions are producing measurable outcomes.

Possible intervention indicators include:

Academic counseling
Attendance support
Mentoring
Welfare assistance
Financial support
Student engagement programs

The analytics layer can compare outcomes before and after intervention where the available dataset supports such analysis.

This helps institutions move from:

"How many students received support?"

to:

"What impact did the support have?"

💼 Business Insights

The platform converts raw student information into decision-support insights.

Example
Observation:
A department has a retention rate below the institutional average.

Supporting indicators:
- Lower average attendance
- Higher academic-risk population
- Increased intervention requirements

Potential Action:
Prioritize academic advising, mentoring, and welfare support
for students showing multiple risk indicators.

The system focuses on identifying patterns that can support institutional decision-making rather than simply displaying raw statistics.

🌍 Impact & Scalability

The platform can support:

Educational institutions
Universities
Colleges
Academic administrators
Faculty advisors
Student welfare departments
Institutional planning teams

Potential benefits include:

Earlier identification of students needing support
Better allocation of welfare resources
Data-driven intervention planning
Improved visibility into retention patterns
Measurement of intervention effectiveness
Faster access to institutional insights

The architecture can be extended to additional institutions and larger student datasets.

🔮 Future Scope

The platform can be extended with:

Real-time student-risk monitoring
Automated intervention recommendations
Explainable AI for risk predictions
Personalized student-support recommendations
Early-warning notifications
Learning Management System integration
Student engagement analytics
Scholarship and financial-aid analysis
Placement and internship analytics
Longitudinal student journey analysis
Advanced AI-powered institutional analytics
🔐 Responsible Data Usage

Student data can contain sensitive information.

The platform should therefore follow responsible data practices:

Use anonymized or synthetic data where appropriate
Avoid unnecessary personally identifiable information
Protect sensitive student records
Restrict access to authorized users
Avoid automated decisions that negatively affect students
Use predictive results as decision-support indicators

The system is intended to support human decision-making, not replace academic or welfare professionals.

🛠️ Technology Stack
Data Engineering
Python
Pandas
SQL
DuckDB
Analytics
Python
SQL
Plotly
Machine Learning
Scikit-learn
Dashboard
Streamlit
Plotly
AI Analyst
Open-source / Local LLM
Natural Language Processing
SQL Generation
Rule-based fallback
Development
Git
GitHub
Python Virtual Environment
Automated Testing
📁 Project Structure
Student-Retention-Welfare-Tracker-01/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── .env.example
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
├── src/
│   ├── data/
│   ├── analytics/
│   ├── ml/
│   ├── agent/
│   └── utils/
│
├── app/
│   ├── streamlit_app.py
│   ├── components/
│   └── pages/
│
├── api/
│   ├── main.py
│   └── routes/
│
├── tests/
│
└── scripts/
    ├── generate_messy_data.py
    ├── clean_data.py
    ├── build_database.py
    └── train_model.py
🔁 Reproducible Pipeline

The project is designed around a reproducible processing pipeline.

# Prepare the dataset
python scripts/generate_messy_data.py

# Clean and validate the data
python scripts/clean_data.py

# Build the analytics database
python scripts/build_database.py

# Train the machine-learning model
python scripts/train_model.py

# Start the dashboard
streamlit run app/streamlit_app.py

The final commands may vary depending on the implemented project configuration.

📋 Data Dictionary

The project maintains documentation describing the fields used by the analytics pipeline.

Typical attributes may include:

Field	Description
Student ID	Unique student identifier
Name	Student name
Department	Academic department
Semester	Current semester
Attendance	Attendance percentage
CGPA	Academic performance indicator
Backlogs	Number of academic backlogs
Retention Status	Student retention outcome
Welfare Support	Welfare support indicator
Intervention	Intervention information
Risk Level	Analytical risk category

The final data dictionary will reflect the actual fields present in the organizer-provided dataset.

🧪 Testing

The project includes tests for important components including:

Data cleaning
Data validation
Analytics calculations
SQL queries
Risk analysis
AI-agent behavior

Testing helps ensure that the data pipeline and analytical outputs remain reliable and reproducible.

🏆 Project Goal

Our goal is to transform messy educational data into actionable intelligence that helps institutions identify student risks earlier, evaluate welfare interventions, and make better student-support decisions.

The platform aims to move education analytics from:

Reactive Support → Proactive Intelligence

Clean the data. Understand the risk. Measure the impact. Support students earlier.

🏫 Hackathon

Track: Education & EdTech

Problem Statement:
Student Retention & Welfare Efficacy Tracker

Event:
TransOrg AgentIQ Datathon — From Messy Data to Agentic Insights

📄 License

This project is licensed under the MIT License.

See the LICENSE file for details.

⭐ Project Vision

From messy student data to proactive student support.

