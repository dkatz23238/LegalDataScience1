import pandas as pd
import numpy as np


def get_concepts():
    concepts = [
        "foreign_exchange", "cost_of_living_adjustment", "contingency",
        "expenses", "termination", "jurisdiction"
    ]
    return concepts


def get_probas():
    probs = [0.2, 0.4, 0.6, 0.7, 0.4, 0.2]
    return probs


def get_risks_from_concepts(concepts):
    return [c + "_risk" for c in concepts]


def get_clauses_from_concepts(concepts):
    return [c + "_clause" for c in concepts]


# Amount of good contracts
X1 = 10000
# Amount of bad contracts
X2 = 2000

random_obs = np.random.randint(1, 7, X1)

contracts = [[np.random.binomial(1, j) for i, j in enumerate(get_probas())]
             for i in range(X1)]

risks = pd.DataFrame(contracts)
clauses = pd.DataFrame(contracts)

contracts_df = pd.concat([risks, clauses], axis=1)
contracts_df.columns = get_risks_from_concepts(
    get_concepts()) + get_clauses_from_concepts(get_concepts())

bad_contracts = [
    [np.random.binomial(1, j)
     for i, j in enumerate(get_probas())] + [0, 0, 0, 0, 0, 0]
    for i in range(X2)
]

bad_contracts_df = pd.DataFrame(bad_contracts, columns=contracts_df.columns)
bad_contracts_df["label"] = 1  # Bad

contracts_df["label"] = 0  # Good

dataset = pd.concat([
    contracts_df,
    bad_contracts_df,
]).sample(X1 + X2).reset_index(drop=True)
dataset.index.name = "index"
dataset.to_csv("dataset.csv")