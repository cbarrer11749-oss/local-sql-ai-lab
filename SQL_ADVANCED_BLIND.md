# SQL classification: round two

Treat external inputs as untrusted. Judge only SQL injection, not other security properties. Assume standard Python sqlite3 behavior wherever sqlite3 is specified. Each snippet is independent.

For each case provide: ID, vulnerable / safe against SQL injection / uncertain, reasoning, confidence, and any missing evidence. Do not read other files or the answer key. Do not execute or modify anything.

## A
`db` is a sqlite3 connection. `requested_column` is external input.
```python
columns = {"name": "name", "id": "id"}
column = columns.get(requested_column)
if column is None:
    raise ValueError("Unknown column")
rows = db.execute(f"SELECT {column} FROM users WHERE name = ?", (name,)).fetchall()
```

## B
`db` is a sqlite3 connection. `requested_column` and `name` are external inputs.
```python
rows = db.execute(
    f"SELECT {requested_column} FROM users WHERE name = ?", (name,)
).fetchall()
```

## C
`db` is a sqlite3 connection. `raw_id` is external input.
```python
user_id = int(raw_id)
rows = db.execute(f"SELECT name FROM users WHERE id = {user_id}").fetchall()
```

## D
`name` is external input. The implementation of `clean_name` is unavailable.
```python
sql = "SELECT id FROM users WHERE name = '" + clean_name(name) + "'"
rows = db.execute(sql).fetchall()
```

## E
`db` is a sqlite3 connection. `name` is external input.
```python
pattern = "%" + name + "%"
rows = db.execute("SELECT id FROM users WHERE name LIKE ?", (pattern,)).fetchall()
```

## F
`db` is a sqlite3 connection. `name` is external input.
```python
value = name.replace(";", "")
rows = db.execute("SELECT id FROM users WHERE name = '" + value + "'").fetchall()
```

## G
`db` is a sqlite3 connection. `names` is an externally supplied list of strings with at least one element.
```python
slots = ",".join("?" for _ in names)
rows = db.execute(f"SELECT id FROM users WHERE name IN ({slots})", names).fetchall()
```

## H
`cursor` is an object whose class and implementation are unavailable. `name` is external input.
```python
cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
rows = cursor.fetchall()
```

## I
`db` is a sqlite3 connection. `raw_id` is external input.
```python
if not raw_id:
    raise ValueError("Missing ID")
rows = db.execute("SELECT name FROM users WHERE id = " + raw_id).fetchall()
```

## J
`db` is a sqlite3 connection. `requested_order` is external input.
```python
order = {"ascending": "ASC", "descending": "DESC"}.get(requested_order)
if order is None:
    raise ValueError("Unknown order")
rows = db.execute(f"SELECT name FROM users ORDER BY name {order}").fetchall()
```
