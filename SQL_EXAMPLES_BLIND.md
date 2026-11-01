# Blind SQL Classification Exercise

Classify each snippet as either `vulnerable` or `correctly parameterized`. Do not open `SQL_EXAMPLES_ANSWER_KEY.md` until you have recorded all six classifications.

Assume `name` is supplied by a user. Each snippet shows how a query is constructed or executed; focus on whether the value is kept separate from SQL syntax.

## Example 1

```python
sql = "SELECT id, name FROM users WHERE name = '" + name + "'"
rows = db.execute(sql).fetchall()
```

## Example 2

```python
sql = "SELECT id, name FROM users WHERE name = ?"
rows = db.execute(sql, (name,)).fetchall()
```

## Example 3

```python
sql = f"SELECT id, name FROM users WHERE name = '{name}'"
rows = db.execute(sql).fetchall()
```

## Example 4

```python
sql = "SELECT id, name FROM users WHERE name = %s"
cursor.execute(sql, (name,))
rows = cursor.fetchall()
```

## Example 5

```python
sql = "SELECT id, name FROM users WHERE name = '%s'" % name
cursor.execute(sql)
rows = cursor.fetchall()
```

## Example 6

```python
sql = "SELECT id, name FROM users WHERE name = :name"
rows = db.execute(sql, {"name": name}).fetchall()
```
