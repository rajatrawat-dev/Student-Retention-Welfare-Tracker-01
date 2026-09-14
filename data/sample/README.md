# StudentIQ Sample Data Directory

This folder documents the synthetic messy data generation and instructions for jury / evaluator dataset substitution.

## Generating Synthetic Data
Run from repository root:
```bash
python scripts/generate_messy_data.py
```
This generates `data/raw/messy_students.csv` containing deliberate anomalies:
- Inconsistent IDs (e.g. `STU-1001`, `stu_1001`, `1001`)
- Noisy department names (e.g. `cse`, `Computer Sci`, `comp sci`, `ECE`, `MECH`)
- Inconsistent gender labels (`M`, `male`, `boy`, `female`, `f`, `girl`)
- Malformed attendance (`85%`, `0.85`, `85`, `72 %`, out-of-bounds numbers)
- Corrupted CGPA formats (`8.5`, `8,5`, `12.0`, `-1.5`, missing values)
- Multiple date conventions (`YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`)
- Duplicate rows and anomalous edge cases

## Evaluating Organizer Datasets
To evaluate with external test datasets:
1. Place the test CSV file at `data/raw/messy_students.csv`.
2. Run data rescue:
   ```bash
   python scripts/clean_data.py
   ```
3. Ingest into DuckDB:
   ```bash
   python scripts/build_database.py
   ```
4. Recalibrate risk models:
   ```bash
   python scripts/train_model.py
   ```
The canonical schema is automatically populated and validated.
