import pyblp
import numpy as np
import pandas as pd

# PyBLP basic logit tutorial

pyblp.options.digits = 5
pyblp.options.verbose = False
pyblp.__version__

product_data = pd.read_csv(pyblp.data.NEVO_PRODUCTS_LOCATION)
products = product_data['product_ids'].unique()
product_effects = pd.DataFrame()
product_effects['product_ids'] = products
product_effects['product_effect'] = product_effects.index 
product_data = product_data.merge(product_effects)
print(product_data[product_data['product_ids'] == 'F3B14'].head())

logit_formulation = pyblp.Formulation('0 + prices', absorb= 'C(market_ids) + C(product_ids)')
logit_formulation

problem = pyblp.Problem(logit_formulation, product_data)
problem


logit_results = problem.solve()

elasticities = logit_results.compute_elasticities(name='prices')
means = logit_results.extract_diagonal_means(elasticities)
print(f"Elasticity {np.mean(means)}")
