import pandas as pd
import re
table_file = '/Users/pryang/Documents/資料庫系統-從SQL到NoSQL/DataFrame/Auto-Tables-Benchmark/ATBench/explode/explode_test25/data.csv'
data = pd.read_csv(table_file)
def isComposite(val: str):
    """Check if value is composite value"""
    date_pattern = re.compile(r'(\d{4}/\d{2}/\d{2})|(\d{2}/\d{2}/\d{4})')
    if date_pattern.match(str(val)):
        return False
    else:
        return ',' in str(val) or '/' in str(val) or "|" in str(val)
    

def isExplode(table_file: str) -> bool:
    data = pd.read_csv(table_file)
    for col in data.columns:
        if data[col].apply(isComposite).any():
            return True
    return False
print(isExplode(table_file))