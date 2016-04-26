#!/usr/bin/python
# vim: set fileencoding=latin-1:

import financers
import candidates
import voters
from operator import methodcaller

num_voters = 1000
num_candidates = 100
open_positions = int(num_candidates * .1)
percentage_with_chances = .2
num_financers = 200
num_periods = 5
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

        # Making all candidates new for this election
        for i in a_candidates:
            i.election_fail()

        # Donation
        for f in a_financers:
            receiver = financers.random.choice(a_candidates)
            receiver.update_treasure(f.donate(percentage))

        # Donation reinforcement
        elite = []
        for h in a_candidates:
            if h.get_total_elections() > 0:
                elite.append(h)

        for g in a_financers:
            if len(elite) > 0:
                receiver = financers.random.choice(elite)
                receiver.update_treasure(g.donate(.1))

        # Election
        a_candidates.sort(key=methodcaller('get_treasure'), reverse=True)

        j = int(positions * (1 + percentage_with_chances))
        this_term = positions
        while this_term > 0:
            c = financers.random.choice(a_candidates[:j])
            if c.get_elected_status() is False:
                c.election_success()
                this_term -= 1

run_the_game(num_periods, my_voters, my_candidates, my_financers, percentage_to_donate, open_positions)

# Printing

print("Parametros")
print('Numero eleitores %s, Candidatos %s, Financiadores %s, Periodos %s, Vagas %s' %
      (num_voters, num_candidates, num_financers, num_periods, open_positions))
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
