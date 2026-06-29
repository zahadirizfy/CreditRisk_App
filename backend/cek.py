import pandas as pd

df = pd.read_csv("dataset/data-training.csv", delimiter=";")

print(df.head())

print(df.columns.tolist())
