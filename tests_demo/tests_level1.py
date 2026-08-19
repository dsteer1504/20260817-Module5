import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calculation = Calculator(8,2)
        answer = calculation.get_sum()
        self.assertEqual(answer, 10, "The sum is wrong.")

    
    def test_multi(self):
        calculation = Calculator(8,2)
        answer = calculation.multi
        self.assertEqual(answer, 16, "The multiplication is wrong")


    def test_division(self):
        calculation = Calculator(8,2)
        answer = calculation.division
        self.assertEqual(answer, 4, "The division is wrong")

    def test_subtraction(self):
        calculation = Calculator(8,2)
        answer = calculation.subtraction
        self.assertEqual(answer, 6, "The subtraction is wrong")

if __name__ == "__main__":
    unittest.main()