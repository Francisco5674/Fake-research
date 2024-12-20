import pandas as pd
import numpy as np
from product_data import import_product_data
from estimation import estimate

def range_vector(x):
    return(x.max() - x.min())

def min_range_vector(x):
    if len(x) > 1:
        x = x.unique()
        x = pd.Series(x)
        x = x.sort_values()
        value = np.min(x.diff())
        return(value)
    else:
        return(0)

def med_distance(x):
    if len(x) > 1:
        x = x.unique()
        x = pd.Series(x)
        x = 1/x
        x = x.sort_values()
        dif = x.diff()
        dif = dif.dropna()
        value = np.median(dif)
        return(value)
    else:
        return(0)

def look_initial_alpha(product_data):
    markets = product_data.groupby("market_ids").agg({'shares': 'sum'})
    markets['s0'] = 1 - markets['shares']
    markets = markets.drop(columns = 'shares')
    product_data_copy = product_data.copy()
    product_data_copy = product_data_copy.merge(markets, left_on='market_ids', right_on='market_ids')
    product_data_copy['logdif'] = np.log(product_data_copy['shares']) - np.log(product_data_copy['s0'])

    products = product_data_copy.groupby('product_ids').agg({'prices':[range_vector,min_range_vector, med_distance],
                                                            'logdif':[range_vector,min_range_vector],
                                                            'market_ids':'count'})

    max_prices = np.max(product_data_copy['prices'])

    print(f"{distance}, {1/max_prices}")


if __name__ == "__main__":
    product_data = import_product_data("src/CL/pyblp.csv")
    look_initial_alpha(product_data)
