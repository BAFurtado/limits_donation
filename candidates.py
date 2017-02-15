import citizens


class Candidates(citizens.Citizens):

    def start(self):
        self.treasure = 0
        self.elected = False
        self.total_elections = 0

    # Record new status
    def election_success(self):
        self.elected = True
        self.update_mandates()

    def election_fail(self):
        self.elected = False

    # Update information
    def update_mandates(self):
        self.total_elections += 1

    def update_treasure(self, amount):
        self.treasure += amount

    def update_income(self, amount):
        self.income += amount

    def get_treasure(self):
        return self.treasure

    def get_elected_status(self):
        return self.elected

    def get_total_elections(self):
        return self.total_elections

    @classmethod
    def convert_to_candidate(cls, obj):
        obj.__class__ = Candidates

    def __str__(self):
        return 'Candidato {} Caixa de Campanha {:.2f}'.format(self.id, self.treasure)