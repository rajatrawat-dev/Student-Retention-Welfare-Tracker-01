# StudentIQ Data Dictionary

## 1. Raw Input Schema (`data/raw/messy_students.csv`)
Simulates noisy real-world data collection issues:

| Raw Column | Common Variations / Defects | Example Values |
|---|---|---|
| `Student ID` | Leading/trailing spaces, mixed case, numeric roll numbers | `STU-1001`, `stu_1001`, ` 1001 ` |
| `Student Name` | Mixed casing, double spaces, punctuation | `aditya sharma`, `  POOJA   PATEL  ` |
| `Department` | Acronyms, abbreviations, colloquial names | `cse`, `comp sci`, `MECH`, `electronics` |
| `Gender` | Inconsistent categories, abbreviations | `M`, `male`, `boy`, `female`, `F`, `girl` |
| `CGPA` | Comma decimals, out-of-bounds (>10 or <0), string nulls | `7,85`, `14.5`, `-1.5`, `NA`, `None` |
| `Attendance Rate` | Decimal fractions, percentage signs, typos | `0.85`, `85%`, ` 72 % `, `850` |
| `Admission Date` | Inconsistent date formats, unparseable dates | `2023-08-01`, `15/08/2023`, `invalid` |

## 2. Canonical Output Schema (`data/processed/cleaned_students.csv`)
Standardized ground-truth structure:

| Canonical Column | Data Type | Permitted Values / Range | Description |
|---|---|---|---|
| `student_id` | String | `STU-XXXX` | Formatted unique student identifier |
| `name` | String | Title Case Text | Normalized student name |
| `department` | String | Standardized 6 Departments | Full academic department name |
| `gender` | String | `Male`, `Female`, `Other` | Standardized gender taxonomy |
| `cgpa` | Float | `0.0` - `10.0` | Validated cumulative grade point average |
| `attendance` | Float | `0.0` - `100.0` | Percentage of lectures attended |
| `enrollment_date` | String (ISO) | `YYYY-MM-DD` | Normalized ISO admission date |
| `attendance_percentage` | Float | `0.0` - `100.0` | Duplicate alias for attendance |
| `academic_risk_score` | Float | `0.0` - `100.0` | Continuous risk penalty score |
| `risk_level` | String | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` | Categorical retention risk classification |
| `support_priority` | String | `Routine`, `Monitor`, `Advisory`, `Immediate Intervention` | Actionable welfare prioritization queue |