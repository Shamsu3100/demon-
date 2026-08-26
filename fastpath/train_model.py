"""Trains a small model and saves it to model.pkl

In the workshop this is a Jupyter notebook. Same code either way:
make data, train, check, save.
"""
import random

import joblib
from sklearn.tree import DecisionTreeClassifier


def label(value, low, high):
    """The rule we want the model to learn from examples."""
    if low <= value <= high:
        return "normal"
    margin = (high - low) / 2 or 1
    if value < low - margin or value > high + margin:
        return "critical"
    return "warning"


def features(value, low, high):
    """Where the reading sits in its safe range.

    0.0 = at the bottom of the range, 1.0 = at the top,
    negative = below it, above 1 = over it.

    Giving the model this one number instead of three raw ones lets it
    compare a body temperature and a motor temperature the same way.
    """
    span = (high - low) or 1
    return [(value - low) / span]


# 1. Make some training data
random.seed(0)
X, y = [], []
for _ in range(3000):
    low = random.uniform(0, 500)
    high = low + random.uniform(1, 500)
    value = random.uniform(low - (high - low), high + (high - low))
    X.append(features(value, low, high))
    y.append(label(value, low, high))

# 2. Train on most of it
model = DecisionTreeClassifier(max_depth=6).fit(X[:2500], y[:2500])

# 3. Check it on data it has never seen
print(f"accuracy on unseen data: {model.score(X[2500:], y[2500:]):.1%}")

# 4. Save it. This file IS the model.
joblib.dump(model, "model.pkl")
print("saved model.pkl")
