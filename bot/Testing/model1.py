import os
from tensorflow.keras.models import load_model
import numpy as np

# Testing the Prakrit Model
model = load_model(os.path.join("Models", "prakriti.keras"))
print(model.summary())
target = ["Vata", "Pitta", "Kapha", "vata+pitta", "vata+kapha", "pitta+kapha"]

# prediction on model
res = model.predict(
    np.array([[0, 0, 2, 0, 1, 1, 2, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 2, 0]])
)
print(res)

index = np.argmax(res)
print("index= ", target[index])
