class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_sum(self):
        return self.a + self.b

    def multi(self):
        return self.a * self.b

    def subtraction(self):
        return self.a - self.b
    
    def division(self):
        return self.a / self.b


if __name__ == "__main__":
    myCalc = Calculator(a=145,b=12)
    print(myCalc.division())

