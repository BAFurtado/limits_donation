from numpy import random

# Empirical data              http://exame.abril.com.br/brasil/campanhas-tem-duas-vezes-mais-candidatos-que-doadores/
# Model parameters
p_donors = 0.0016  # % of general universe
p_candidates = 0.0028  # % of general universe

num_citizens = 100000
num_candidates = int(num_citizens * p_candidates)
num_donors = int(num_citizens * p_donors)
number_runs = 10

income_percentage_case1 = .1
ceiling_amount = .05

# Parameters Beta distribution chosen to reflect a GINI coefficient of around .47
income_list = random.beta(1, 8, num_citizens)
