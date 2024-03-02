import os
from joblib import load
import joblib
import numpy as np

# Testing the Prakrit Model
model = load(os.path.join("Models/prakriti"))

target = ["Vata", "Pitta", "Kapha", "vata+pitta", "vata+kapha", "pitta+kapha"]

# prediction on model
res = model.predict(
    np.array([[2, 1, 0, 2, 1, 0, 2, 0, 1, 0, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0]])
)
print(res)

index = np.argmax(res)
print("index= ", target[index])