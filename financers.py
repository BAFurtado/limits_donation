import random


class Financers:
    def __init__(self, id):
        self.id = id
        self.income = random.gauss(50, 20)

    def donate(self, percentage):
        return self.income * percentage

    def __str__(self):
        return 'Financiador %s Renda %.2f' % (self.id, self.income)
