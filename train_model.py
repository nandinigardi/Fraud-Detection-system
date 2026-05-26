import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# LOAD DATA
df = pd.read_csv("transactions.csv")

# FEATURES
df["Foreign"] = df["Location"].apply(lambda x: 1 if x != "India" else 0)
df["High_Amount"] = df["Amount"].apply(lambda x: 1 if x > 50000 else 0)

type_map = {"ATM": 0, "Card": 1, "Online": 2, "International": 3}
df["Transaction_Type"] = df["Transaction_Type"].map(type_map)

X = df[[
    "Amount",
    "Time_Risk",
    "Transaction_Type",
    "Frequency",
    "Foreign",
    "High_Amount"
]]

y = df["Status"]

# SPLIT
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# MODEL
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# ACCURACY
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print("Model Accuracy:", acc)

# SAVE MODEL
with open("fraud_model.pkl", "wb") as f:
    pickle.dump(model, f)