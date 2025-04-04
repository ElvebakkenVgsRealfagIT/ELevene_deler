import pandas as pd

fil_csv = "Datasett_fodselstall.csv"

df = pd.read_csv(fil_csv, encoding="utf-8-sig", delimiter="\t")

df["Innflyttinger"] = pd.to_numeric(df["Innflyttinger"], errors="coerce")
df["Utflyttinger"] = pd.to_numeric(df["Utflyttinger"], errors="coerce")
df["Levendefødte i alt"] = pd.to_numeric(df["Levendefødte i alt"], errors="coerce")
df["Nettovekst"] = df["Levendefødte i alt"] + df["Innflyttinger"] - df["Utflyttinger"]