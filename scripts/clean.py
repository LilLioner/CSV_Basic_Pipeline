import pandas as pd
import numpy as np
from pathlib import Path

raw = Path("data/raw")
psd = Path("data/processed")


psd.mkdir(exist_ok=True)
          
csv_raw = raw.glob("*.csv")

for i in csv_raw:
  df = pd.read_csv(i)
  print(df)