# ==========================================
# THERMOSIM AI
# RANDOM FOREST TEMPERATURE PREDICTOR
# ==========================================

import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import GroupShuffleSplit

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==========================================
# 1. LOAD TRAINING DATA
# ==========================================

print("\nLoading THERMOSIM AI dataset...")

df = pd.read_csv("data/simulation_data.csv")

print("Dataset loaded successfully!")

print("Total records:", len(df))


# ==========================================
# 2. SELECT INPUT FEATURES
# ==========================================

features = [

    "current",

    "ambient_temp",

    "initial_cold_temp",

    "initial_hot_temp",

    "internal_heat_load",

    "time"

]

targets = [

    "cold_temperature",

    "hot_temperature"

]

X = df[features]

Y = df[targets]


# ==========================================
# 3. SPLIT BY OPERATING CONDITIONS
# ==========================================

# Keep complete simulation runs together.
# This tests performance on unseen conditions.

groups = (
    df["current"].astype(str) + "_" +
    df["ambient_temp"].astype(str) + "_" +
    df["internal_heat_load"].astype(str)
)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_indices, test_indices = next(
    splitter.split(X, Y, groups)
)

X_train = X.iloc[train_indices]
X_test = X.iloc[test_indices]

Y_train = Y.iloc[train_indices]
Y_test = Y.iloc[test_indices]


print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ==========================================
# 4. CREATE RANDOM FOREST MODEL
# ==========================================

print("\nCreating Random Forest model...")


model = RandomForestRegressor(

    n_estimators=200,

    max_depth=20,

    min_samples_split=2,

    random_state=42,

    n_jobs=-1

)


# ==========================================
# 5. TRAIN THE MODEL
# ==========================================

print("\nTraining AI model...")

model.fit(X_train, Y_train)

print("Training completed!")


# ==========================================
# 6. MAKE PREDICTIONS
# ==========================================

predictions = model.predict(X_test)


# ==========================================
# 7. EVALUATE MODEL
# ==========================================

cold_actual = Y_test["cold_temperature"]

hot_actual = Y_test["hot_temperature"]

cold_predicted = predictions[:, 0]

hot_predicted = predictions[:, 1]


cold_mae = mean_absolute_error(
    cold_actual,
    cold_predicted
)

hot_mae = mean_absolute_error(
    hot_actual,
    hot_predicted
)


cold_rmse = np.sqrt(
    mean_squared_error(
        cold_actual,
        cold_predicted
    )
)

hot_rmse = np.sqrt(
    mean_squared_error(
        hot_actual,
        hot_predicted
    )
)


cold_r2 = r2_score(
    cold_actual,
    cold_predicted
)

hot_r2 = r2_score(
    hot_actual,
    hot_predicted
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n====================================")
print(" THERMOSIM AI - MODEL PERFORMANCE")
print("====================================")

print("\nCOLD-SIDE PREDICTION")

print("MAE:", round(cold_mae, 4), "°C")

print("RMSE:", round(cold_rmse, 4), "°C")

print("R2 Score:", round(cold_r2, 4))


print("\nHOT-SIDE PREDICTION")

print("MAE:", round(hot_mae, 4), "°C")

print("RMSE:", round(hot_rmse, 4), "°C")

print("R2 Score:", round(hot_r2, 4))


# ==========================================
# 9. SAVE TRAINED MODEL
# ==========================================

os.makedirs("models", exist_ok=True)

model_package = {

    "model": model,

    "features": features,

    "targets": targets,

    "validation": {

        "cold_mae": cold_mae,

        "hot_mae": hot_mae,

        "cold_rmse": cold_rmse,

        "hot_rmse": hot_rmse,

        "cold_r2": cold_r2,

        "hot_r2": hot_r2

    }

}


joblib.dump(
    model_package,
    "models/temperature_model.joblib"
)


print("\nAI MODEL SAVED SUCCESSFULLY!")

print("Location: models/temperature_model.joblib")

print("\nTHERMOSIM AI TRAINING COMPLETED!")