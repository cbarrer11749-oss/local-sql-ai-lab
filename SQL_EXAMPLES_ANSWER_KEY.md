# Answer Key — Blind SQL Classification Exercise

Do not provide this file to the model before it classifies the snippets in `SQL_EXAMPLES_BLIND.md`.

| Example | Classification | Reason |
|---|---|---|
| 1 | Vulnerable | Concatenates the user value into SQL text before execution. |
| 2 | Correctly parameterized | The `?` placeholder is bound separately to the value tuple. |
| 3 | Vulnerable | The f-string interpolates the user value into the SQL text. |
| 4 | Correctly parameterized | `%s` is a driver placeholder, and the value is passed separately to `execute`. |
| 5 | Vulnerable | Python `%` formatting inserts the value into SQL before execution; it is not parameter binding. |
| 6 | Correctly parameterized | The named placeholder is bound separately through a parameter mapping. |

The three vulnerable snippets mix user data into SQL syntax. The three correctly parameterized snippets pass the value separately to the database driver, which treats it as data rather than executable SQL. Exact placeholder syntax varies by database driver; use that driver's documented parameter-binding interface and do not add quotes around placeholders unless its documentation specifically requires them.
