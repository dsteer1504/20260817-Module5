import pandas as pd
import unittest
from Clean_Customers import days_between


class TestDaysBetween(unittest.TestCase):

    def setUp(self):
        self.borrowing = pd.DataFrame({
            "checkout": ["22/02/2022","01/06/2023","32/05/2023"],
            "returned": ["28/02/2022","01/06/2023","04/06/2023"],
        })
        
    def test_counts_whole_days(self):
        result = days_between(self.borrowing, "checkout","returned", "days")
        self.assertEqual(result.loc[0, "days"],6,"Days Between Calculation Incorrect")

    def test_same_day_is_zero(self):
        result = days_between(self.borrowing, "checkout","returned", "days")
        self.assertEqual(result.loc[1, "days"],0,"Same Day Return not equal 0")

    def test_invalid_date_gives_null(self):
        result = days_between(self.borrowing, "checkout","returned", "days")
        self.assertTrue(pd.isna(result.loc[2, "days"],),"invalid date",)


if __name__ == "__main__":
    unittest.main()