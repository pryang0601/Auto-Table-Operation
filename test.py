import pandas as pd
data = pd.read_csv("/Users/pryang/Documents/資料庫系統-從SQL到NoSQL/DataFrame/Auto-Tables-Benchmark/ATBench/stack/ATBench/ffill/ffill_test1/data.csv")
data = data.ffill(axis=0)
print(data)