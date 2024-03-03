import os
from joblib import load
import numpy as np

# Testing the Prakrit Model
model = load(os.path.join("Models/prakriti"))

target = ["Vata", "Pitta", "Kapha", "vata+pitta", "vata+kapha", "pitta+kapha"]

# prediction on model
res = model.predict(
    np.array([[0,0,2,0,1,1,2,0,0,0,0,1,1,1,0,1,1,1,2,0]])
)
print(res)

index = np.argmax(res)
print("index= ", target[index])