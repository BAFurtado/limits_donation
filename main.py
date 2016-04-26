#!/usr/bin/python
# vim: set fileencoding=latin-1:

import financers
import candidates
import voters
from operator import methodcaller

num_voters = 1000
num_candidates = 100
open_positions = int(num_candidates * .1)
num_financers = 200
num_periods = 10
percentage_to_donate = financers.random.random()

# Generate agents


def generate(nv, nc, nf):
    my_voters = []
    my_candidates = []
    my_financers = []
    for voter in range(nv):
        my_voters.append(voters.Voters(voter))
    for candidate in range(nc):
        my_candidates.append(candidates.Candidates(candidate))
    for financer in range(nf):
        my_financers.append(financers.Financers(financer))
    return my_voters, my_candidates, my_financers

my_voters, my_candidates, my_financers = generate(num_voters, num_candidates, num_financers)


# Initiate time frame


def run_the_game(periods, a_voters, a_candidates, a_financers, percentage, positions):
    for period in range(periods):
        # Donation
        for f in a_financers:
            receiver = financers.random.choice(a_candidates)
            receiver.update_treasure(f.donate(percentage))

        # Election
        a_candidates.sort(key=methodcaller('get_treasure'), reverse=True)

        for i in range(len(a_candidates)):
            if i < positions:
                a_candidates[i].election_success()
            else:
                a_candidates[i].election_fail()



run_the_game(num_periods, my_voters, my_candidates, my_financers, percentage_to_donate, open_positions)

# Printing

print("Parametros")
print('Numero eleitores %s, Candidatos %s, Financiadores %s, Periodos %s, Vagas %s, Percentual doacao %s' %
      (num_voters, num_candidates, num_financers, num_periods, open_positions, percentage_to_donate))
print("---")
print("Amostra de resultados")
for i in range(4):
    print(my_voters[i])

print("---")
print('Candidatos eleitos')
my_candidates.sort(key=methodcaller('get_total_elections'), reverse=True)

for candidate in my_candidates:
    if candidate.get_total_elections() > 0:
        print(candidate)

print("---")
for i in range(4):
    print(my_financers[i])
