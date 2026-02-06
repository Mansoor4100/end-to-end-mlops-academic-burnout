import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to DB
conn = sqlite3.connect("burnout.db")

# Load predictions table
df = pd.read_sql("SELECT * FROM predictions", conn)
conn.close()

print(df.head())

# -----------------------------
# Chart 1: Burnout distribution
# -----------------------------
plt.figure()
df["burnout_prediction"].value_counts().plot(kind="bar")
plt.title("Burnout Prediction Distribution")
plt.xlabel("Burnout (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.show()

# -----------------------------
# Chart 2: Probability histogram
# -----------------------------
plt.figure()
df["burnout_probability"].hist(bins=10)
plt.title("Burnout Probability Distribution")
plt.xlabel("Probability")
plt.ylabel("Frequency")
plt.show()
