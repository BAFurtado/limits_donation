import citizens


class Financers(citizens.Citizens):

    def cumulative_donation(self, amount):
        self.total_donated += amount

    def donate(self, percentage=None, amount=None):
        if amount is None:
            self.cumulative_donation(self.income * percentage)
            r = self.income * percentage
            self.income -= self.income * percentage
            return r
        else:
            if self.income >= amount:
                self.cumulative_donation(amount)
                self.income -= amount
                return amount
            else:
                r = self.income
                self.income = 0
                return r

    def get_cumulative_donation(self):
        return self.total_donated

    def reset_total_donated(self):
        self.total_donated = 0

    @classmethod
    def convert_to_donor(cls, obj):
        # if obj.__class__ == Candidates:
        #     print('Another donor who is a candidate')
        obj.__class__ = Financers

    def __str__(self):
        return 'Doador {} Renda {:.2f} Total doado {:.4f}'.format(self.id, self.income, self.total_donated)
