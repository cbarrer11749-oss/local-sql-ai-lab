SQL injection repair exercise (B, F, I)

All examples and tests use a local in-memory sqlite3 database populated only
with fictitious users Alice and Bob. Run from this directory:

    python3 -m unittest -v test_sql_repairs.py

B — Fixed allowlist for column selection
`search_by_column` maps the caller's requested key to one of two hard-coded
column identifiers (`name` or `id`) and rejects anything else. Column names
cannot be supplied as sqlite3 bound parameters, so only the trusted allowlist
value is interpolated. The name used in the WHERE clause is bound separately.
Tests cover legitimate selection of both allowed columns and rejection of a
query-shaped column value.

F — Bind the name instead of concatenating it
`find_by_name` uses a `?` placeholder and supplies the external name in the
parameter tuple. A quote/comment payload is therefore treated as a literal
name, not as SQL syntax. Tests cover an ordinary lookup and the payload,
which returns no rows rather than changing the predicate.

I — Validate integer form and bind the ID
`find_by_id` converts the external string to an integer, rejecting malformed
values, then supplies the integer through a `?` placeholder. The SQL text stays
fixed. Tests cover a valid ID and the former `0 OR 1=1` style payload, which is
rejected; the fictitious table remains unchanged.
