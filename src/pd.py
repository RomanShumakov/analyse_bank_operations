import json

import pandas as pd
from config import PATH_TO_OPERATIONS

df = pd.read_excel(PATH_TO_OPERATIONS)
df = df[df["Сумма операции"] < 0]

total_df = df[["Категория", "Сумма операции"]].groupby("Категория").sum().reset_index()

data = total_df.to_dict("records")
print(json.dumps(data, ensure_ascii=False, indent=4))
