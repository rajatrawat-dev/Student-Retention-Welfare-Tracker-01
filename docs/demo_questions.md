# StudentIQ Curated Demo Questions for Datathon Presentation

Use these validated questions to demonstrate the four layers of StudentIQ to the judges.

| # | Question Prompt | Detected Intent | Generated DuckDB SQL | Recommended Visualization |
|---|---|---|---|---|
| 1 | `Show students with attendance below 60%.` | `ATTENDANCE_QUERY` | `SELECT student_id, name, department, attendance, cgpa, risk_level FROM students WHERE attendance < 60.0 ORDER BY attendance ASC LIMIT 20;` | Tabular + Critical Badges |
| 2 | `Which departments have the lowest average CGPA?` | `DEPARTMENT_QUERY` | `SELECT department, ROUND(AVG(cgpa), 2) as avg_cgpa, COUNT(*) as student_count FROM students GROUP BY department ORDER BY avg_cgpa ASC;` | Bar Chart |
| 3 | `Compare CSE, ECE and IT.` | `DEPARTMENT_QUERY` | `SELECT department, COUNT(*) as student_count, ROUND(AVG(cgpa), 2) as avg_cgpa, ROUND(AVG(attendance), 2) as avg_attendance, SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_students FROM students GROUP BY department ORDER BY avg_cgpa DESC;` | Comparative Dual-Axis Bar Chart |
| 4 | `Show the relationship between attendance and CGPA.` | `CORRELATION_QUERY` | `SELECT student_id, name, department, attendance, cgpa, risk_level FROM students ORDER BY cgpa DESC LIMIT 100;` | Scatter Plot with Risk Legend |
| 5 | `Which students are at high risk?` | `RISK_QUERY` | `SELECT student_id, name, department, cgpa, attendance, academic_risk_score, risk_level, support_priority FROM students WHERE risk_level IN ('HIGH', 'CRITICAL') ORDER BY academic_risk_score DESC LIMIT 25;` | Styled Table with Badges |
| 6 | `Show the distribution of student risk.` | `DISTRIBUTION_QUERY` | `SELECT risk_level, COUNT(*) as student_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM students), 1) as percentage FROM students GROUP BY risk_level ORDER BY student_count DESC;` | Donut Chart |
| 7 | `Which department needs the most academic support?` | `DEPARTMENT_QUERY` | `SELECT department, SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as at_risk_count, ROUND(SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as at_risk_percentage, ROUND(AVG(academic_risk_score), 2) as avg_risk_score FROM students GROUP BY department ORDER BY at_risk_count DESC;` | Risk Heatmap Bar Chart |
| 8 | `Show top 10 students by CGPA.` | `TOP_PERFORMERS` | `SELECT student_id, name, department, cgpa, attendance, risk_level FROM students ORDER BY cgpa DESC, attendance DESC LIMIT 10;` | Horizontal Ranking Bar Chart |