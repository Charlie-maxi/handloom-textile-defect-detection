import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("outputs", exist_ok=True)

# Replace these values with your actual confusion matrix if different
cm = np.array([
    [326, 7],
    [6, 209]
])

fig, ax = plt.subplots(figsize=(6,5))

im = ax.imshow(cm)

ax.set_xticks([0,1])
ax.set_yticks([0,1])

ax.set_xticklabels(["No Defect","Defect"])
ax.set_yticklabels(["No Defect","Defect"])

for i in range(2):
    for j in range(2):
        ax.text(
            j,
            i,
            cm[i,j],
            ha="center",
            va="center"
        )

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.savefig(
    "outputs/confusion_matrix.png",
    bbox_inches="tight"
)

plt.show()

print("Confusion Matrix Saved!")