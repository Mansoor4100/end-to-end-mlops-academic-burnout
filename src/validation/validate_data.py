import os
import pandas as pd
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "validation", "schema.yaml")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "student_activity_processed.csv")

with open(SCHEMA_PATH, "r") as f:
    schema = yaml.safe_load(f)

df = pd.read_csv(DATA_PATH)
schema_columns = schema["columns"].keys()
data_columns = df.columns.tolist()

missing_cols = set(schema_columns) - set(data_columns)
extra_cols = set(data_columns) - set(schema_columns)

if missing_cols:
    raise ValueError(f"Missing columns: {missing_cols}")

if extra_cols:
    print(f"Warning: Extra columns detected: {extra_cols}")
from pandas.api.types import (
    is_integer_dtype,
    is_float_dtype,
    is_string_dtype
)

for col, props in schema["columns"].items():
    expected_type = props["type"]

    if expected_type == "integer" and not is_integer_dtype(df[col]):
        raise TypeError(f"Column {col} expected integer")

    if expected_type == "float" and not is_float_dtype(df[col]):
        raise TypeError(f"Column {col} expected float")

    if expected_type in ["string", "category"] and not is_string_dtype(df[col]):
        raise TypeError(f"Column {col} expected string/category")

null_cols = df.columns[df.isnull().any()].tolist()
if null_cols:
    raise ValueError(f"Null values found in columns: {null_cols}")
target = schema["target_column"]
if target not in df.columns:
    raise ValueError("Target column missing")
