import unittest
import random
from birthday_simulation import has_shared_birthday, simulate, theoretical_probability

class BirthdayTests(unittest.TestCase):
    def test_matching(self):
        self.assertFalse(has_shared_birthday([]))
        self.assertFalse(has_shared_birthday([1, 2, 365]))
        self.assertTrue(has_shared_birthday([1, 365, 1]))
        self.assertTrue(has_shared_birthday([42, 42, 42]))
    def test_boundaries(self):
        for n in [0, 1]:
            self.assertEqual(simulate(n, 20), 0)
            self.assertEqual(theoretical_probability(n), 0)
        self.assertEqual(simulate(366, 20), 1)
        self.assertEqual(theoretical_probability(366), 1)
    def test_exact(self):
        self.assertAlmostEqual(theoretical_probability(2), 1/365)
        self.assertAlmostEqual(theoretical_probability(23), .5072972343)
        self.assertLess(theoretical_probability(22), .5)
    def test_simulation_agreement(self):
        for n in [10, 23, 30]:
            self.assertLess(abs(simulate(n, 10000, random.Random(217))-theoretical_probability(n)), .02)
    def test_reproducibility(self):
        self.assertEqual(simulate(23, 100, random.Random(217)), simulate(23, 100, random.Random(217)))
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): simulate(-1)
        with self.assertRaises(ValueError): simulate(23, 0)
        with self.assertRaises(ValueError): theoretical_probability(-1)

if __name__ == '__main__': unittest.main()
