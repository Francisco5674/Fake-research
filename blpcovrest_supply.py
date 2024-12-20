import pyblp
import numpy as np
import pandas as pd

pyblp.options.digits = 5
pyblp.options.verbose = False
pyblp.__version__

product_data = pd.read_csv(pyblp.data.BLP_PRODUCTS_LOCATION)
# product_data['covariance_instruments0'] = 1
print(product_data.columns)
# product_data = product_data.drop(columns=['demand_instruments0',
#                            'demand_instruments1',
#                            'demand_instruments2',
#                            'demand_instruments3',
#                            'demand_instruments4',
#                            'demand_instruments5',
#                            'demand_instruments6',
#                            'demand_instruments7'])

agent_data = pd.read_csv(pyblp.data.BLP_AGENTS_LOCATION)

print(product_data.columns)


product_formulations = (
   pyblp.Formulation('1 + hpwt + air + mpd + space'),
   pyblp.Formulation('1 + prices + hpwt + air + mpd + space'),
   pyblp.Formulation('1 + log(hpwt) + air + log(mpg) + log(space) + trend')
)


agent_formulation = pyblp.Formulation('0 + I(1 / income)')

problem = pyblp.Problem(product_formulations, product_data, agent_formulation, agent_data, costs_type='log')
print(problem)

initial_sigma = np.diag([3.612, 0, 4.628, 1.818, 1.050, 2.056])
initial_pi = np.c_[[0, -43.501, 0, 0, 0, 0]]

results = problem.solve(
    initial_sigma,
    initial_pi,
    costs_bounds=(0.001, None),
    W_type='clustered',
    se_type='clustered',
    initial_update=True,
)

# print(results.compute_elasticities(name='prices', market_id=None))

elasticities = results.compute_elasticities(name='prices')
means = results.extract_diagonal_means(elasticities)
print(np.mean(means))
