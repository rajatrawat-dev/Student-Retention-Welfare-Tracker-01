"""Normalizer functions for cleaning noisy student data attributes."""

import re
from typing import Any, Optional, Tuple
import pandas as pd
import numpy as np

# Department alias mapping
DEPT_MAPPING = {
    "cse": "Computer Science & Engineering",
    "cs": "Computer Science & Engineering",
    "comp sci": "Computer Science & Engineering",
    "computer science": "Computer Science & Engineering",
    "computer science & engineering": "Computer Science & Engineering",
    "computer science and engineering": "Computer Science & Engineering",
    "ece": "Electronics & Communication Engineering",
    "electronics": "Electronics & Communication Engineering",
    "electronics & communication": "Electronics & Communication Engineering",
    "electronics and comm": "Electronics & Communication Engineering",
    "electronics & communication engineering": "Electronics & Communication Engineering",
    "me": "Mechanical Engineering",
    "mech": "Mechanical Engineering",
    "mechanical": "Mechanical Engineering",
    "mechanical engineering": "Mechanical Engineering",
    "ce": "Civil Engineering",
    "civil": "Civil Engineering",
    "civ": "Civil Engineering",
    "civil engineering": "Civil Engineering",
    "it": "Information Technology",
    "info tech": "Information Technology",
    "information tech": "Information Technology",
    "information technology": "Information Technology",
    "ee": "Electrical Engineering",
    "eee": "Electrical Engineering",
    "electrical": "Electrical Engineering",
    "electrical engineering": "Electrical Engineering",
}

GENDER_MAPPING = {
    "m": "Male",
    "male": "Male",
    "boy": "Male",
    "man": "Male",
    "f": "Female",
    "female": "Female",
    "girl": "Female",
    "woman": "Female",
    "o": "Other",
    "other": "Other",
    "non-binary": "Other",
    "nb": "Other",
}

def normalize_student_id(val: Any) -> Tuple[Optional[str], bool]:
    """Normalizes student IDs into standard format STU-XXXX.
    Returns (cleaned_id, was_modified).
    """
    if pd.isna(val) or val is None:
        return None, False
    s = str(val).strip().upper()
    orig = str(val)
    
    # Extract any sequence of digits
    digits_match = re.search(r'(\d+)', s)
    if digits_match:
        num = int(digits_match.group(1))
        standardized = f"STU-{num:04d}"
        return standardized, (orig != standardized)
    
    # Fallback to sanitized alphanumeric
    cleaned = re.sub(r'[^A-Z0-9-]', '', s)
    return cleaned if cleaned else None, (orig != cleaned)

def normalize_name(val: Any) -> Tuple[Optional[str], bool]:
    """Cleans student names: removes odd characters, standardizes casing."""
    if pd.isna(val) or val is None:
        return None, False
    orig = str(val)
    s = orig.strip()
    # Remove extra spaces and special punctuation
    s = re.sub(r"[^a-zA-Z\s\.-]", "", s)
    s = re.sub(r"\s+", " ", s)
    cleaned = s.title().strip()
    return cleaned if cleaned else None, (orig != cleaned)

def normalize_department(val: Any) -> Tuple[str, bool]:
    """Maps department variations to canonical department names."""
    if pd.isna(val) or val is None:
        return "Unknown Department", True
    orig = str(val)
    s = orig.strip().lower()
    s = re.sub(r'[^a-z0-9\s&]', '', s)
    s = re.sub(r'\s+', ' ', s)
    
    if s in DEPT_MAPPING:
        return DEPT_MAPPING[s], (orig != DEPT_MAPPING[s])
    
    # Fuzzy keyword check
    for key, canonical in DEPT_MAPPING.items():
        if key in s.split():
            return canonical, True
            
    return orig.strip().title(), False

def normalize_gender(val: Any) -> Tuple[str, bool]:
    """Normalizes gender values to Male, Female, Other, or Unknown."""
    if pd.isna(val) or val is None:
        return "Unknown", True
    orig = str(val)
    s = orig.strip().lower()
    cleaned = GENDER_MAPPING.get(s, "Other")
    return cleaned, (orig != cleaned)

def normalize_attendance(val: Any) -> Tuple[Optional[float], bool]:
    """Normalizes diverse attendance inputs (e.g. '85%', 0.85, '85', '  72 %  ').
    Standardizes output to 0.0 - 100.0 scale.
    """
    if pd.isna(val) or val is None:
        return None, False
    orig = str(val)
    s = orig.strip()
    
    # Remove % sign and spaces
    has_percent = "%" in s
    s_clean = s.replace("%", "").strip()
    
    try:
        num = float(s_clean)
        modified = False
        
        # If represented as ratio e.g. 0.85 (and <= 1.0)
        if 0.0 < num <= 1.0 and not has_percent:
            num = num * 100.0
            modified = True
            
        # Outlier / bounds handling
        if num < 0.0:
            num = 0.0
            modified = True
        elif num > 100.0:
            # Check if typo like 850 or 880
            if num <= 1000.0 and (num / 10.0) <= 100.0:
                num = num / 10.0
            else:
                num = 100.0
            modified = True
            
        return round(num, 2), modified or has_percent or (orig != str(num))
    except (ValueError, TypeError):
        return None, True

def normalize_cgpa(val: Any) -> Tuple[Optional[float], bool]:
    """Validates and standardizes CGPA on a 0.0 - 10.0 scale."""
    if pd.isna(val) or val is None:
        return None, False
    orig = str(val)
    s = orig.strip().replace(",", ".")
    
    try:
        num = float(s)
        modified = (orig != str(num))
        # Handle out of range
        if num < 0.0 or num > 10.0:
            # Impossible CGPA
            return None, True
        return round(num, 2), modified
    except (ValueError, TypeError):
        return None, True

def normalize_date(val: Any) -> Tuple[Optional[str], bool]:
    """Parses various date conventions to standard ISO YYYY-MM-DD."""
    if pd.isna(val) or val is None:
        return None, False
    orig = str(val).strip()
    
    # Try parsing via pandas to_datetime
    try:
        # Common formats
        parsed = pd.to_datetime(orig, errors="coerce")
        if pd.isna(parsed):
            return None, True
        iso_str = parsed.strftime("%Y-%m-%d")
        return iso_str, (orig != iso_str)
    except Exception:
        return None, True
