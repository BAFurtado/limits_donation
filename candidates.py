class Candidates:

    def __init__(self, id):
        self.id = id
        self.treasure = 0
        self.elected = False
        self.total_elections = 0
        self.income = 0

    # Retrieve information
    def get_treasure(self):
        return self.treasure

    def get_elected_status(self):
        return self.elected

    def get_total_elections(self):
        return self.total_elections

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

    def __str__(self):
        return 'Candidato %s, Numero mandatos %s, Caixa %.2f' % (self.id, self.get_total_elections(), self.treasure)
