

class Citizens:

    def __init__(self, ID, income):
        self.id = ID
        self.income = income

    # Retrieve information
    def get_income(self):
        return self.income

    def __str__(self):
        return 'Cidadão {}, Renda {:.2f}'.format(self.id, self.income)
