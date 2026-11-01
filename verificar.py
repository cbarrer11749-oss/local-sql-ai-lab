"""Check vulnerable and parameterized behavior without opening network ports."""
import unittest
from app import buscar


class Tests(unittest.TestCase):
    def test_legitimate_search(self):
        for seguro in (False, True):
            self.assertEqual(buscar('ana', seguro), [(1, 'ana')])

    def test_injection_and_parameterized_query(self):
        payload = "' OR '1'='1"
        self.assertEqual(len(buscar(payload, False)), 3)
        self.assertEqual(buscar(payload, True), [])

    def test_quote_is_data_in_parameterized_mode(self):
        self.assertEqual(buscar("O'Brien", True), [])


if __name__ == '__main__':
    unittest.main()
