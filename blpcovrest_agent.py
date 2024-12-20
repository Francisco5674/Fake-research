import pyblp
import pandas as pd
import numpy as np

# Load the Nevo cereal data
product_data = pd.read_csv(pyblp.data.NEVO_PRODUCTS_LOCATION)
agent_data = pd.read_csv(pyblp.data.NEVO_AGENTS_LOCATION)

# Create covariance 'instruments'
product_data['covariance_instruments0'] = 1
product_data = product_data[['market_ids','brand_ids','firm_ids',
                             'city_ids','quarter','product_ids','shares', 
                             'prices','mushy','sugar', 'demand_instruments0']]
products = product_data['product_ids'].unique()
product_effects = pd.DataFrame()
product_effects['product_ids'] = products
product_effects['product_effect'] = product_effects.index
product_data = product_data.merge(product_effects)
product_data['random'] = np.random.randint(1, 100, product_data.shape[0])

# Formulations

X1_formulation = pyblp.Formulation('0 + random', absorb= 'C(market_ids) + C(product_ids)')
X2_formulation = pyblp.Formulation('0 + I(-prices)')
# X3_formulation = pyblp.Formulation('0 + random', absorb= 'C(market_ids) + C(product_ids)')
agent_formulation = pyblp.Formulation('1')
product_formulations = (X1_formulation, X2_formulation)

# Set up and solve the problem
mc_problem = pyblp.Problem(
    product_formulations,
    product_data,
    agent_formulation,
    agent_data
)


initial_sigma = np.diag([0])
initial_pi = np.diag([2.8])

# bfgs = pyblp.Optimization('bfgs', {'gtol': 1e-4})
results = mc_problem.solve(
    initial_sigma,
    initial_pi,
    costs_bounds=(0, None),
    initial_update=True
)


# Elasticities
elasticities = results.compute_elasticities(name='prices')
means = results.extract_diagonal_means(elasticities)
print(f"Elasticity {np.mean(means)}")


# # Checking covariance(xi, omega)
# doublecheck = results.to_dict(attributes= ['xi','omega'])
# xi = list(map( lambda x: x[0] ,doublecheck['xi']))
# omega = list(map( lambda x: x[0] ,doublecheck['omega']))
# mean_xi = sum(xi) / len(xi)
# mean_omega = sum(omega) / len(omega)
# print("Cov(xi,omega)")
# print(sum((xi - mean_xi) * (omega - mean_omega) for (xi,omega) in zip(xi,omega)) / len(xi))
