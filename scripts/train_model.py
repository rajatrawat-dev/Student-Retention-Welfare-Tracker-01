"""Trains the Student Retention Risk ML Model."""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ml.train import train_and_save_model
from src.config.settings import settings

def run_training():
    print("==================================================")
    print("      STUDENTIQ -- RETENTION RISK ML TRAINING     ")
    print("==================================================")
    
    metrics = train_and_save_model()
    
    status = metrics.get("status")
    print(f"Status:            {status}")
    print(f"Message:           {metrics.get('message')}")
    
    if status == "DATASET_TOO_SMALL":
        print("Note: Dataset too small for statistically reliable model evaluation.")
        print("Calibrated transparent rule-based risk classifier as active fallback.")
    else:
        print(f"Accuracy:          {metrics.get('accuracy')}")
        print(f"F1-Macro:          {metrics.get('f1_macro')}")
        print(f"Training Samples:  {metrics.get('n_train')}")
        print(f"Test Samples:      {metrics.get('n_test')}")
        
    print(f"Model serialized:  {settings.MODEL_PATH}")
    print("==================================================")

if __name__ == "__main__":
    run_training()