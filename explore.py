import pandas as pd
df = pd.read_csv("BasicCompanyData-2026-09-01-part1_7.csv")
#for random companies
sample = df.sample(n=25, random_state=42)
# print(df.head())
# print(df.columns.tolist())
print(sample[['CompanyName',' CompanyNumber']])
