import time

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from numpy import random, mean, median

import GiniCoef
import candidates
import citizens
import financers
import parameters
import os


# Generate agents
def generate_citizens(num_cit, inc_list):
    my_citizens = []
    for i in range(num_cit):
        my_citizens.append(citizens.Citizens(i, inc_list[i]))
    return my_citizens


def reset_universe(ag, num_candidates, num_donors):
    # Choosing candidates and signing-in with TSE ;)
    cand_ = random.choice(ag, num_candidates)
    # Converting Citizens into Candidates class
    [candidates.Candidates.convert_to_candidate(c) for c in cand_]
    # Initiating Candidates variables
    [c.start() for c in cand_]
    # Selecting donors from general population
    don_ = random.choice(ag, num_donors)
    # Excluding Candidates from the Donors base
    don_ = [d for d in don_ if not isinstance(d, candidates.Candidates)]
    # Converting Citizens into Donors class
    [financers.Financers.convert_to_donor(d) for d in don_]
    return cand_, don_


# Initiate simulation
def run_the_game(my_agents, num_candidates, num_donors):

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

        cand_, don_ = reset_universe(my_agents, num_candidates, num_donors)
        print('Number of candidates {}'.format(len(cand_)))
        print('Number of donors {}'.format(len(don_)))
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
                a = random.uniform(0, 1)
                c.update_treasure(d.donate(amount=a))
        gini, m = call_plot([d.get_cumulative_donation() for d in don_], each, cases[each][2])
        average_gini[each].append(gini)
        average_donation[each].append(m)

    return average_gini, average_donation


def call_plot(values, case, color):
    some_results = GiniCoef.Gini(values)
    print("{} GINI is {:.4f}".format(case, some_results[0]))
    m = median(values)
    lw = .1
    if case == 'Ex-ante':
        lw = 1.5
        print('Renda mediana - {}: {:.4f}'.format(case, m))
    else:
        print('Valor doação mediano - {}: {:.4f}'.format(case, m))

    # Plot
    plt.plot([0, 100], [0, 100], '--', color='yellow')
    plt.plot(some_results[1][0], some_results[1][1], color=color, label=case, lw=lw)
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
        gini, donation = run_the_game(my_agents, parameters.num_candidates, parameters.num_donors)
        print('')
        print('Total citizens {}'.format(len(my_agents)))

        print('')
        print('Time spent in seconds {:.2f}'.format(time.time() - start))
        for each in gini.keys():
            average_gini[each].append(gini[each])
            average_donation[each].append(donation[each])

    # General output
    m_g_1 = median(average_gini['Case 1 Percentage ceiling'])
    m_d_1 = median(average_donation['Case 1 Percentage ceiling'])
    m_g_2 = median(average_gini['Case 2 Nominal ceiling'])
    m_d_2 = median(average_donation['Case 2 Nominal ceiling'])
    m_g_3 = median(average_gini['Case 3 No ceiling'])
    m_d_3 = median(average_donation['Case 3 No ceiling'])

    print('')
    print('Overall Gini averages')
    print('Case 1 Percentage ceiling: median Gini {:.4} Donated value median {:.4}'.format(m_g_1, m_d_1))
    print('Case 2 Nominal ceiling: median Gini {:.4} Donated value {:.4}'.format(m_g_2, m_d_2))
    print('Case 3 No ceiling: median Gini{:.4} Donated value median {:.4}'
          .format(m_g_3, m_d_3))

    with open('output.csv', 'a') as f:
        f.write('perc_{}_nominal_{}\n'.format(parameters.income_percentage_case1, parameters.ceiling_amount))
        f.write('{:.12f};{:.12f}\n'.format(m_g_1, m_d_1))
        f.write('{:.12f};{:.12f}\n'.format(m_g_2, m_d_2))
        f.write('{:.12f};{:.12f}\n'.format(m_g_3, m_d_3))

    dark_patch = mpatches.Patch(color='black', label='Ex-ante pop. income')
    blue_patch = mpatches.Patch(color='blue', label='Case 1 Percentage ceiling: {}%'
                                .format(parameters.income_percentage_case1 * 100))
    red_patch = mpatches.Patch(color='red', label='Case 2 Nominal ceiling: {}'.format(parameters.ceiling_amount))
    green_patch = mpatches.Patch(color='green', label='Case 3 No ceiling')

    plt.legend(handles=[dark_patch, blue_patch, red_patch, green_patch], loc='upper left', frameon=False)
    plt.savefig('figures_png/fig_perc{}_nom{}.png'
                .format(parameters.income_percentage_case1, parameters.ceiling_amount),
                format='png')
    plt.savefig('figures_pdf/fig_perc{}_nom{}.pdf'
                .format(parameters.income_percentage_case1, parameters.ceiling_amount),
                format='pdf', transparent=True)


def overriding_parameters():
    if os.path.exists('output.csv'):
        os.remove('output.csv')
    perc = [.05, .1, .2, .3]
    nominal = [.01, .05, .1, .25]
    for i in range(len(perc)):
        parameters.income_percentage_case1 = perc[i]
        parameters.ceiling_amount = nominal[i]
        repetition()


if __name__ == '__main__':
    # Adjust parameters in parameters.py
    # Call the simulation
    # repetition()

    # To run multiple comparatives, use the function below and set them in the respective function above
    overriding_parameters()


