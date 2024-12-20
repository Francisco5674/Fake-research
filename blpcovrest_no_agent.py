import pyblp
import pandas as pd
import numpy as np

# Load the Nevo cereal data
product_data = pd.read_csv(pyblp.data.NEVO_PRODUCTS_LOCATION)

# Create covariance 'instruments'
product_data['covariance_instruments0'] = 1
product_data = product_data[['market_ids','brand_ids','firm_ids',
                             'city_ids','quarter','product_ids','shares', 
                             'prices','mushy','sugar', 'covariance_instruments0']]

# PyBLP will automatically use instruments


X1_formulation = pyblp.Formulation('0 + C(product_ids)')
X2_formulation = pyblp.Formulation('0 + I(-prices)')
X3_formulation = pyblp.Formulation('0 + C(product_ids)')
product_formulations = (X1_formulation, X2_formulation, X3_formulation)

mc_integration = pyblp.Integration('monte_carlo', size=50, specification_options={'seed': 0})
# Set up and solve the problem
mc_problem = pyblp.Problem(
    product_formulations,
    product_data, 
    integration=mc_integration,
    rc_types = ["log"]
)


initial_sigma = np.diag([1])

# bfgs = pyblp.Optimization('bfgs', {'gtol': 1e-4})
results = mc_problem.solve(
    initial_sigma,
    costs_bounds=(0, None),
    initial_update=True
)

elasticities = results.compute_elasticities(name='prices')
means = results.extract_diagonal_means(elasticities)
print(np.mean(means))


