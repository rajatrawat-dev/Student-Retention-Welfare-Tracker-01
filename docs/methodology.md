# StudentIQ Methodology & Risk Scoring Formulation

## 1. 14-Step Data Rescue Methodology

The Data Rescue layer applies deterministic and probabilistic cleansing:
1. **Encoding Tolerant Ingestion**: Automatically tries UTF-8 and Latin-1 encodings.
2. **Header Normalization**: Fuzzy regex maps varying header aliases (`reg_no`, `branch`, `gpa`) to canonical names.
3. **Exact Row Deduplication**: Drops identical record snapshots.
4. **Identifier Standardization & Collision Resolution**: Normalizes IDs to `STU-XXXX`. Resolves duplicate keys by preserving the record with higher completeness.
5. **Name Cleansing**: Strips numbers/symbols, collapses whitespace, standardizes to title case.
6. **Department Alias Resolution**: Dictionary & keyword mapping normalizes 20+ variations into 6 accredited engineering branches.
7. **Gender Categorization**: Maps heterogeneous gender markers into `Male`, `Female`, or `Other`.
8. **Attendance Normalization**: Parses ratios (`0.85 -> 85.0`), removes `%`, divides 10x typos (`850 -> 85.0`), clamps to `[0, 100]`.
9. **CGPA Bounds Enforcement**: Replaces comma decimals, rejects impossible values (<0 or >10) and converts to `NaN`.
10. **ISO Date Normalization**: Multi-format datetime parser converts dates into ISO `YYYY-MM-DD`.
11. **Department-Median Imputation**: Missing continuous values (`cgpa`, `attendance`) are imputed with the median of the student's department.
12. **Academic Anomaly Detection**: Identifies cognitive dissonance (e.g. CGPA > 9.5 with attendance < 30%).
13. **Derived Feature Engineering**: Computes composite academic risk scores and triage priority.
14. **Composite Quality Scoring**: Measures dataset completeness, uniqueness, validity, and consistency on a 0-100 scale.

## 2. Academic Risk Scoring Formulation

Continuous composite academic risk score ($S_{risk}$) ranges from 0 to 100:

$$S_{risk} = \left(\frac{10.0 - \text{CGPA}}{10.0}\right) \times 60 + \left(\frac{100.0 - \text{Attendance}}{100.0}\right) \times 40$$

- **CGPA Penalty**: Accounts for 60% weight of retention vulnerability.
- **Attendance Penalty**: Accounts for 40% weight of retention vulnerability.

### Tier Cutoffs
- **CRITICAL**: $S_{risk} \ge 55$ OR Attendance $< 60\%$ OR CGPA $< 4.5$
- **HIGH**: $S_{risk} \ge 40$ OR Attendance $< 75\%$ OR CGPA $< 6.0$
- **MEDIUM**: $S_{risk} \ge 25$
- **LOW**: Otherwise

## 3. AI Safety Layer & Copilot Protocol

The AI Analyst is safeguarded against prompt injection and data mutation:
- **Strict Read-Only Enforcement**: Rejects any non-SELECT statements.
- **AST / Regex Lexical Gatekeeper**: Rejects `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `PRAGMA`, semicolons, and multi-statement payloads.
- **Entity Whitelisting**: Restricts queries exclusively to approved tables (`students`) and views (`department_summary`, `risk_summary`).
- **Autonomous Fallback**: If an external LLM (Ollama) is offline or generates invalid syntax, the deterministic query engine responds in sub-millisecond time.