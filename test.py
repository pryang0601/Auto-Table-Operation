import pandas as pd
import numpy as np
table_file = "/Users/pryang/Documents/資料庫系統-從SQL到NoSQL/DataFrame/Auto-Tables-Benchmark/ATBench/stack/ATBench/subtitle/subtitle_test1/data.csv"
data = pd.read_csv(table_file)
columns = data.columns
# drop empty columns
empty_columns = data.columns[data.isnull().all()]
if not empty_columns.empty:
    data.drop(empty_columns, axis=1, inplace=True)
#get subtitles
mask = data.iloc[:, 1:].isna().all(axis=1)
print(len(mask))
subtitles = data[columns[0]][mask]
indexes = list(subtitles.index)
subtitles = list(subtitles)
data.insert(0, "Subtitle", np.NAN)
for idx,index in enumerate(indexes):
    data.iloc[index, 0] = subtitles[idx]
data.fillna(method="ffill", inplace= True)
data.drop(axis=0, index=indexes, inplace= True)
print(data)

