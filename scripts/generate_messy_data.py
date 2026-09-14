"""Generates a realistic synthetic messy student dataset.
Simulates real-world data collection defects without using any real student identities.
"""

import random
import csv
from pathlib import Path
import pandas as pd
import numpy as np

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "messy_students.csv"

# Synthetic name pools
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
    "Shaurya", "Atharva", "Advik", "Pranav", "Advaith", "Kabir", "Ananya", "Diya", "Saanvi", "Aadhya",
    "Pari", "Anika", "Navya", "Angel", "Myra", "Riya", "Aarohi", "Meera", "Sara", "Isha", "Rohan", "Pooja"
]
LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Reddy", "Gupta", "Nair", "Iyer", "Kumar", "Singh", "Mishra",
    "Choudhury", "Bose", "Das", "Menon", "Joshi", "Mehta", "Bhat", "Pillai", "Rao", "Deshmukh"
]

DEPT_VARIANTS = [
    "Computer Science & Engineering", "cse", "CS", "comp sci", "computer science",
    "Electronics & Communication Engineering", "ece", "electronics", "electronics and comm",
    "Mechanical Engineering", "mech", "ME", "mechanical",
    "Civil Engineering", "civil", "CE", "civ",
    "Information Technology", "it", "info tech", "information technology",
    "Electrical Engineering", "ee", "eee", "electrical"
]

GENDER_VARIANTS = ["Male", "M", "male", "boy", "Female", "F", "female", "girl", "Other", "non-binary"]

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%Y/%m/%d"]

def generate_messy_dataset(num_records: int = 650):
    random.seed(42)
    np.random.seed(42)
    
    rows = []
    
    for i in range(1, num_records + 1):
        # 1. Messy ID variations
        id_style = random.choice(["standard", "lowercase", "raw_num", "prefix_space"])
        if id_style == "standard":
            stu_id = f"STU-{1000 + i}"
        elif id_style == "lowercase":
            stu_id = f"stu_{1000 + i}"
        elif id_style == "raw_num":
            stu_id = f"{1000 + i}"
        else:
            stu_id = f"  STU-{1000 + i}  "

        # 2. Name with occasional whitespace or casing defects
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        name_style = random.choice(["clean", "upper", "lower", "messy_space"])
        if name_style == "clean":
            name = f"{fname} {lname}"
        elif name_style == "upper":
            name = f"{fname.upper()} {lname.upper()}"
        elif name_style == "lower":
            name = f"{fname.lower()} {lname.lower()}"
        else:
            name = f"  {fname}   {lname}  "

        # 3. Department with aliases and dirty casing
        dept = random.choice(DEPT_VARIANTS)
        if random.random() < 0.15:
            dept = f"  {dept}  "

        # 4. Gender variations
        gender = random.choice(GENDER_VARIANTS)

        # 5. CGPA with missing values, commas, out-of-bounds
        cgpa_rand = random.random()
        if cgpa_rand < 0.06:
            cgpa = None # Missing
        elif cgpa_rand < 0.10:
            cgpa = "NA" # String null
        elif cgpa_rand < 0.13:
            # Out of bounds
            cgpa = random.choice([-1.5, 12.5, 15.0])
        elif cgpa_rand < 0.20:
            # Comma format e.g. 7,85
            val = round(random.uniform(4.0, 9.8), 2)
            cgpa = str(val).replace(".", ",")
        else:
            # Standard numeric with occasional whitespace
            val = round(random.uniform(3.5, 9.9), 2)
            cgpa = f" {val} " if random.random() < 0.1 else val

        # 6. Attendance variations (percentages, decimals, integers, strings)
        att_rand = random.random()
        if att_rand < 0.05:
            att = None
        elif att_rand < 0.15:
            # Ratio e.g. 0.82
            att = round(random.uniform(0.40, 0.99), 2)
        elif att_rand < 0.35:
            # Percent string e.g. "85%" or " 72 % "
            val = int(random.uniform(45, 98))
            att = f"{val}%" if random.random() < 0.5 else f" {val} % "
        elif att_rand < 0.40:
            # Out of bounds or typo e.g. 850
            att = random.choice([-5, 850, 110])
        else:
            # Standard number
            att = round(random.uniform(40.0, 99.0), 1)

        # 7. Date formatting variations
        date_rand = random.random()
        base_dt = pd.Timestamp("2023-08-01") + pd.Timedelta(days=random.randint(0, 400))
        if date_rand < 0.04:
            enroll_dt = "invalid-date"
        elif date_rand < 0.06:
            enroll_dt = None
        else:
            fmt = random.choice(DATE_FORMATS)
            enroll_dt = base_dt.strftime(fmt)

        # 8. Deliberate Suspicious Anomaly (e.g. 9.8 CGPA with 15% attendance)
        if random.random() < 0.02:
            cgpa = 9.8
            att = "15%"

        rows.append({
            "Student ID": stu_id,
            "Student Name": name,
            "Department": dept,
            "Gender": gender,
            "CGPA": cgpa,
            "Attendance Rate": att,
            "Admission Date": enroll_dt
        })

    # Add deliberate duplicate records (duplicate rows and duplicate IDs)
    duplicates = [rows[i].copy() for i in range(15)]
    rows.extend(duplicates)
    
    # Duplicate IDs with different casing/spacing
    for i in range(10):
        dup_row = rows[i].copy()
        dup_row["Student ID"] = rows[i]["Student ID"].strip().lower()
        rows.append(dup_row)

    random.shuffle(rows)
    
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated synthetic messy dataset with {len(df)} records at {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_messy_dataset()
