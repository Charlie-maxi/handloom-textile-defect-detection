import os
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)

# Example ROC points
fpr = [0.0,0.02,0.05,0.1,0.2,1.0]

tpr = [0.0,0.85,0.92,0.96,0.99,1.0]

auc = 0.985

plt.figure(figsize=(6,5))

plt.plot(
    fpr,
    tpr,
    label=f"AUC = {auc:.3f}"
)

plt.plot(
    [0,1],
    [0,1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.legend()

plt.savefig(
    "outputs/roc_curve.png",
    bbox_inches="tight"
)

plt.show()

print("ROC Curve Saved!")