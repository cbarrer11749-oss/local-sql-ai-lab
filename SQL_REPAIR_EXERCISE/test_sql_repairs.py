import sqlite3
import unittest

from sql_repairs import search_by_column, find_by_name, find_by_id


class SQLRepairTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        self.db.executemany(
            "INSERT INTO users (id, name) VALUES (?, ?)",
            [(1, "Alice"), (2, "Bob")],
        )

    def tearDown(self):
        self.db.close()

    def test_b_legitimate_allowlisted_column(self):
        self.assertEqual(search_by_column(self.db, "name", "Alice"), [("Alice",)])
        self.assertEqual(search_by_column(self.db, "id", "Bob"), [(2,)])

    def test_b_injected_column_is_rejected(self):
        with self.assertRaises(ValueError):
            search_by_column(self.db, "name FROM users --", "Alice")

    def test_b_column_expression_is_rejected(self):
        with self.assertRaises(ValueError):
            search_by_column(self.db, "name || '!' AS name", "Alice")

    def test_f_legitimate_name(self):
        self.assertEqual(find_by_name(self.db, "Alice"), [(1,)])

    def test_f_quote_payload_does_not_change_query(self):
        self.assertEqual(find_by_name(self.db, "' OR 1=1 --"), [])

    def test_i_legitimate_integer_id(self):
        self.assertEqual(find_by_id(self.db, "2"), [("Bob",)])

    def test_i_sql_payload_is_rejected(self):
        with self.assertRaises(ValueError):
            find_by_id(self.db, "0 OR 1=1")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM users").fetchone(), (2,))


if __name__ == "__main__":
    unittest.main()
