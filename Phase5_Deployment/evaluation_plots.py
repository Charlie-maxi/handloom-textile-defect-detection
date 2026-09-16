import os
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)

models = [
    "RF",
    "Bagging",
    "GB",
    "LightGBM",
    "XGBoost",
    "CatBoost",
    "Voting"
]

accuracy = [
    97.08,
    97.63,
    97.45,
    97.63,
    97.81,
    98.54,
    98.54
]

plt.figure(figsize=(10,5))

plt.bar(models, accuracy)

plt.xlabel("Models")

plt.ylabel("Accuracy (%)")

plt.title("Model Accuracy Comparison")

for i, v in enumerate(accuracy):
    plt.text(i, v+0.1, str(v))

plt.savefig("outputs/accuracy_comparison.png")

plt.show()

print("Graph Saved Successfully!")