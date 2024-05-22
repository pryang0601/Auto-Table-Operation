import mysql.connector
import json
with open("config.json") as f:
    config = json.load(f)
host = config["host"]
user = config["user"]
password = config["password"]
db = mysql.connector.connect(
    host = host,
    user = user,
    password = password,
    database = "Files"
)

def insert_file(table: str) -> None:
    cursor = db.cursor()
    query = "INSERT INTO FilePath (table_file) VALUES (%s)"
    cursor.execute(query, (table,))
    db.commit()



def get_file() -> str:
    """Get the last inserted file"""
    cursor = db.cursor()
    query = "SELECT * FROM FilePath ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    last_item = cursor.fetchone()
    return (last_item[0], last_item[1])


def insert_data(ID: int, operation: str, start: int, end: int, output: str) -> None:
    """Insert data into table"""
    cursor = db.cursor()
    query = """
    UPDATE FilePath
    SET operation = %s, start_idx = %s, end_idx = %s, output_file = %s
    WHERE id = %s
    """
    cursor.execute(query, (operation, start, end, output, ID))
    db.commit()