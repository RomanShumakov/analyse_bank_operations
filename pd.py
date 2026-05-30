import pandas as pd
from config import PATH_TO_OPERATIONS

df = pd.read_excel(PATH_TO_OPERATIONS)
df = df[df[Эсумам] < 0]

total_df = def[["Категория", "Сумма операции"]].groupby("Категория").sum().reset_index()
