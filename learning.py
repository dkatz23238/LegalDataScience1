from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import pandas as pd

df = pd.read_csv("dataset.csv").set_index("index")
train_ = df[[i for i in df.columns if i != "label"]]
labels_ = df["label"]

train_X, test_X, train_y, test_y = train_test_split(train_, labels_)

model = LogisticRegression()
model.fit(train_X, train_y)
print(model.score(test_X, test_y))