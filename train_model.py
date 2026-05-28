import pandas as pd
from sqlalchemy import create_engine

# Machine Learning
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# ==========================================
# DATABASE CONNECTION
# ==========================================

DATABASE_URL = "DATABASE_URL"

engine = create_engine(DATABASE_URL)

# ==========================================
# LOAD DATA
# ==========================================

query = """
SELECT
    o.route_id,
    o.total_distance,
    v.vehicle_age,
    f.refuel_liter
FROM operational_record o
JOIN vehicle v
    ON o.vehicle_id = v.vehicle_id
JOIN fuel_record f
    ON o.vehicle_id = f.vehicle_id
WHERE
    f.refuel_liter IS NOT NULL
"""

df = pd.read_sql(query, engine)

print(df.head())

# ==========================================
# FEATURES & TARGET
# ==========================================

X = df[
    [
        "route_id",
        "total_distance",
        "vehicle_age"
    ]
]

y = df["refuel_liter"]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# TRAIN MODEL
# ==========================================

model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)

# ==========================================
# EVALUATE
# ==========================================

predictions = model.predict(X_test)

from sklearn.metrics import mean_absolute_error, r2_score

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("MAE:", mae)
print("R2 Score:", r2)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(model, "fuel_prediction_model.pkl")

print("Model saved successfully!")
