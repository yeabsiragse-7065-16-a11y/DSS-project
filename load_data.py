import pandas as pd
		# Load dataset
df = pd.read_excel("data/fuel_dataset.xlsx")
		# Display first 5 rows
print(df.head())
print("\nColumns:")
print(df.columns)
print("\nDataset Shape:")
print(df.shape)
print("\nDataset Info:")
print(df.info())
#Standardize Column Names
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")
print(df.columns)
#Check Missing Values
print(df.isnull().sum())
#Basic data cleaning
df = df.dropna()
#Save Cleaned Dataset
df.to_csv("data/cleaned/cleaned_fuel_data.csv", index=False)