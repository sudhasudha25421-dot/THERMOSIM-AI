# ==========================================
# THERMOSIM AI
# TRAINING DATA GENERATION
# ==========================================

import os
import numpy as np
import pandas as pd

from itertools import product

from models.peltier_model import simulate_thermal_response


# Create dataset folder

os.makedirs("data", exist_ok=True)

dataset = []


# Operating conditions

currents = [1, 2, 3, 4, 5]

ambient_temperatures = [20, 25, 30, 35]

heat_loads = [0, 2, 5]


# Generate simulation combinations

combinations = list(product(
    currents,
    ambient_temperatures,
    heat_loads
))

print("Generating training data...")


for current, ambient, heat_load in combinations:

    results = simulate_thermal_response(

        current=current,

        ambient_temp=ambient,

        initial_cold_temp=30,

        initial_hot_temp=30,

        duration=600,

        internal_heat_load=heat_load

    )

    # Store every simulation time point

    for i in range(len(results["time"])):

        dataset.append({

            "current": current,

            "ambient_temp": ambient,

            "initial_cold_temp": 30,

            "initial_hot_temp": 30,

            "internal_heat_load": heat_load,

            "time": results["time"][i],

            "cold_temperature":
                results["cold_temperature"][i],

            "hot_temperature":
                results["hot_temperature"][i]

        })


# Convert to DataFrame

df = pd.DataFrame(dataset)


# Save CSV

df.to_csv(
    "data/simulation_data.csv",
    index=False
)


print("\nDATA GENERATION COMPLETED")

print("Total records:", len(df))

print("\nDataset Preview:")

print(df.head())

print("\nSaved to data/simulation_data.csv")