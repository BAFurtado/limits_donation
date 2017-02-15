import time

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from numpy import random, mean

import GiniCoef
import candidates
import citizens
import financers

# Empirical data              http://exame.abril.com.br/brasil/campanhas-tem-duas-vezes-mais-candidatos-que-doadores/
# Model parameters
p_donors = 0.0016                 # % of general universe
p_candidates = 0.0028             # % of general universe

num_citizens = 100000
num_candidates = int(num_citizens * p_candidates)
num_donors = int(num_citizens * p_donors)

income_percentage_case1 = .1
ceiling_amount = .1

# Parameters Beta distribution chosen to reflect a GINI coefficient of around .47
income_list = random.beta(1, 8, num_citizens)


# Generate agents
def generate_citizens(num_cit, inc_list):
    my_citizens = []
    for i in range(num_cit):
        my_citizens.append(citizens.Citizens(i, inc_list[i]))
    return my_citizens


# Initiate simulation
def run_the_game(my_agents, num_candidates, num_donors):

    # Choosing candidates and signing-in with TSE ;)
    cand_ = random.choice(my_agents, num_candidates)

    # Converting Citizens into Candidates class
    [candidates.Candidates.convert_to_candidate(c) for c in cand_]

    # Initiating Candidates variables
    [c.start() for c in cand_]

    # Selecting donors from general population
    don_ = random.choice(my_agents, num_donors)

    # Excluding Candidates from the Donors base
    don_ = [d for d in don_ if not isinstance(d, candidates.Candidates)]

    # Converting Citizens into Donors class
    [financers.Financers.convert_to_donor(d) for d in don_]

    # Testing three case scenarios
    print('')
    print('Testing three cases')

    cases = {'Case 1 Percentage ceiling': ['Donation ceiling set at 10% of income', income_percentage_case1, 'blue'],
             'Case 2 Nominal ceiling': ['Donation ceiling set at Nominal value of .1', ceiling_amount, 'red'],
             'Case 3 No ceiling': ['Donation with no ceiling', None, 'green']}

    for each in cases.keys():
        print('')
        print('{}: {}'.format(each, cases[each][0]))

        # Reseting total donated
        [d.reset_total_donated() for d in don_]
        # Donation
        percentages = random.random(len(don_))

        for i, d in enumerate(don_):
            c = random.choice(cand_)
            # Donation based on percentage of income or given amount
            if each == 'Case 1 Percentage ceiling':
                c.update_treasure(d.donate(percentage=(percentages[i] * cases[each][1])))
            elif each == 'Case 2 Nominal ceiling':
                a = random.uniform(0, cases[each][1])
                c.update_treasure(d.donate(amount=a))
            else:
                c.update_treasure(d.donate(percentage=(percentages[i])))
        call_plot([d.get_cumulative_donation() for d in don_], each, cases[each][2])
    return (cand_, don_)


# Simulation
# Call agents generation
start = time.time()
my_agents = generate_citizens(num_citizens, income_list)


def call_plot(values, case, color):
    some_results = GiniCoef.Gini(values)

    print("{} GINI is {:.4f}".format(case, some_results[0]))
    if case == 'Ex-ante':
        print('Renda média - {}: {:.4f}'.format(case, mean(values)))
    else:
        print('Valor doação médio - {}: {:.4f}'.format(case, mean(values)))

    # Plot
    plt.plot([0, 100], [0, 100], '--')
    plt.plot(some_results[1][0], some_results[1][1], color=color, label=case)
    plt.xlabel('% of population')
    plt.ylabel('% of values')


# Ex-ante GINI
call_plot(income_list, 'Ex-ante', 'brown')

# Running the game
for i in range(3):
    (cand, don) = run_the_game(my_agents, num_candidates, num_donors)

    print('')
    print('Total citizens {}'.format(len(my_agents)))
    print('Number of candidates {}'.format(len(cand)))
    print('Number of donors {}'.format(len(don)))
    print('')
    print('Time spent in seconds {:.2f}'.format(time.time() - start))

#plt.legend(loc='upper left')

cases = {'Case 1 Percentage ceiling': ['Donation ceiling set at 10% of income', income_percentage_case1, 'darkblue'],
             'Case 2 Nominal ceiling': ['Donation ceiling set at Nominal value of .1', ceiling_amount, 'red'],
             'Case 3 No ceiling': ['Donation with no ceiling', None, 'green']}

blue_patch = mpatches.Patch(color='blue', label='Case 1 Percentage ceiling')
red_patch = mpatches.Patch(color='red', label='Case 2 Nominal ceiling')
green_patch = mpatches.Patch(color='green', label='Case 3 No ceiling')

plt.legend(handles=[blue_patch, red_patch, green_patch])
plt.savefig('p1')
