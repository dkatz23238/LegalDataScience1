from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import pandas as pd
from grakn.client import GraknClient


def get_concepts():
    concepts = [
        "foreign_exchange", "cost_of_living_adjustment", "contingency",
        "expenses", "termination", "jurisdiction"
    ]
    return concepts


df = pd.read_csv("dataset.csv").set_index("index").query(
    'label == 0').iloc[:, 0:6]
df = df[[c for c in df.columns if c != "label"]].head(20)
df.columns = get_concepts()
factor_queries = []

for c in df.columns:
    gql_query = 'insert $risk-factor isa risk-factor, has risk-factor-name "%s";' % c
    gql_query += 'insert $risk-mitigation-clause isa risk-mitigation-clause, has risk-factor-name "%s";' % c
    factor_queries.append(gql_query)

contract_queries = []

for index, contract in df.iterrows():
    gql_query = 'insert $contract isa contract, has contractID "%s";' % index
    contract_queries.append(gql_query)

relation_queries = []
for index, contract in df.iterrows():
    properties = zip(contract.index, contract.values)
    for i, j in properties:
        if j == 1:
            gql_query = 'match  $contract isa contract,    has contractID "%s";' % index
            gql_query += '  $rf isa risk-factor,    has risk-factor-name "%s";' % i
            gql_query += '  $rc isa risk-mitigation-clause,     has risk-factor-name "%s";' % i
            gql_query += 'insert  $contract-risk (contract-has: $contract, contract-risk-factor: $rf) isa contract-risk;'
            gql_query += '  $contract-mitigation (contract-has: $contract, contract-mitigation-clause: $rc) isa contract-mitigation;\n'

        relation_queries.append(gql_query)

with open("insert_factors.gql", "w") as f:
    for i in set(factor_queries):
        f.write(i)


with open("insert_contracts.gql", "w") as f:
    for i in set(contract_queries):
        f.write(i)

with open("insert_relations.gql", "w") as f:
    for i in set(relation_queries):
        f.write(i)
