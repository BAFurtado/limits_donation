import time

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from numpy import random, mean, median

import GiniCoef
import candidates
import citizens
import financers
import parameters


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

    cases = {'Case 1 Percentage ceiling': ['Donation ceiling set at {}% of income'
                                               .format(parameters.income_percentage_case1 * 100),
                                           parameters.income_percentage_case1, 'blue'],
             'Case 2 Nominal ceiling': ['Donation ceiling set at Nominal value of {}'
                                            .format(parameters.ceiling_amount), parameters.ceiling_amount, 'red'],
             'Case 3 No ceiling': ['Donation with no ceiling', None, 'green']}

    average_gini = {'Case 1 Percentage ceiling': [],
                    'Case 2 Nominal ceiling': [],
                    'Case 3 No ceiling': []}

    average_donation = {'Case 1 Percentage ceiling': [],
                    'Case 2 Nominal ceiling': [],
                    'Case 3 No ceiling': []}

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
                # Choosing value from 0 to nominal ceiling
                a = random.uniform(0, cases[each][1])
                c.update_treasure(d.donate(amount=a))
            else:
                c.update_treasure(d.donate(percentage=(percentages[i])))
        gini, m = call_plot([d.get_cumulative_donation() for d in don_], each, cases[each][2])
        average_gini[each].append(gini)
        average_donation[each].append(m)

    return cand_, don_, average_gini, average_donation


def call_plot(values, case, color):
    some_results = GiniCoef.Gini(values)
    print("{} GINI is {:.4f}".format(case, some_results[0]))
    m = median(values)
    if case == 'Ex-ante':
        print('Renda mediana - {}: {:.4f}'.format(case, m))
    else:
        print('Valor doação mediano - {}: {:.4f}'.format(case, m))

    # Plot
    plt.plot([0, 100], [0, 100], '--')
    plt.plot(some_results[1][0], some_results[1][1], color=color, label=case)
    plt.xlabel('% of population')
    plt.ylabel('% of values')
    return some_results[0], m


def repetition():
    # Running the game
    start = time.time()
    my_agents = generate_citizens(parameters.num_citizens, parameters.income_list)
    # Ex-ante GINI
    call_plot(parameters.income_list, 'Ex-ante', 'black')
    # Empty dictionaries
    average_gini = {'Case 1 Percentage ceiling': [],
                    'Case 2 Nominal ceiling': [],
                    'Case 3 No ceiling': []}

    average_donation = {'Case 1 Percentage ceiling': [],
                        'Case 2 Nominal ceiling': [],
                        'Case 3 No ceiling': []}

    # Numerous runs
    for i in range(parameters.number_runs):
        cand, don, gini, donation = run_the_game(my_agents, parameters.num_candidates, parameters.num_donors)
        print('')
        print('Total citizens {}'.format(len(my_agents)))
        print('Number of candidates {}'.format(len(cand)))
        print('Number of donors {}'.format(len(don)))
        print('')
        print('Time spent in seconds {:.2f}'.format(time.time() - start))
        for each in gini.keys():
            average_gini[each].append(gini[each])
            average_donation[each].append(donation[each])

    print('')
    print('Overall Gini averages')
    print('Case 1 Percentage ceiling: median Gini {:.4} Donated value median {:.4}'.format(median(average_gini['Case 1 Percentage ceiling']),
                                                                            median(average_donation['Case 1 Percentage ceiling'])))
    print('Case 2 Nominal ceiling: median Gini {:.4} Donated value {:.4}'.format(median(average_gini['Case 2 Nominal ceiling']),
                                                     median(average_donation['Case 2 Nominal ceiling'])))
    print('Case 3 No ceiling: median Gini{:.4} Donated value median {:.4}'.format(median(average_gini['Case 3 No ceiling']),
                                                median(average_donation['Case 3 No ceiling'])))

    dark_patch = mpatches.Patch(color='black', label='Ex-ante pop. income')
    blue_patch = mpatches.Patch(color='blue', label='Case 1 Percentage ceiling')
    red_patch = mpatches.Patch(color='red', label='Case 2 Nominal ceiling')
    green_patch = mpatches.Patch(color='green', label='Case 3 No ceiling')

    plt.legend(handles=[dark_patch, blue_patch, red_patch, green_patch], loc='upper left')
    plt.savefig('p1')


if __name__ == '__main__':
    # Adjust parameters in parameters.py
    # Call the simulation
    repetition()
