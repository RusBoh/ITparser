import sqlite3


def create_table(cursor: sqlite3.Cursor, name: str, args: dict):
    if len(args) > 1:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {"".join(f"{i} {args[i]},\n" for i in list(args.keys())[:-1])}
                {list(args.keys())[-1]} {args[list(args.keys())[-1]]}
            )
        """)
    else:
        cursor.execute(f"""
            CREATE TABLE {name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {list(args.keys())[0]} {args[list(args.keys())[0]]}
            )
        """)

def del_table(cursor: sqlite3.Cursor, name: str):
    cursor.execute(f"DROP TABLE IF EXISTS {name}")

def add_item(cursor: sqlite3.Cursor, table_name: str, args: dict):
    cursor.execute(f"""
        INSERT INTO {table_name} ({"".join(f"{i}, " for i in args)[:-2]}) VALUES ({"?, " * (len(args) - 1) + "?"})
    """, list(args.values()))