import streamlit as st
import pandas as pd
import joblib
from sqlalchemy import create_engine

# -----------------------------
# DATABASE CONNECTION
# -----------------------------

DATABASE_URL = "DATABASE_URL"

engine = create_engine(DATABASE_URL)

# -----------------------------
# LOAD MODEL
# -----------------------------

model = joblib.load("fuel_prediction_model.pkl")

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("Fuel Request Prediction")

st.write(
    "Predict efficient fuel requirement based on route and vehicle age."
)

# -----------------------------
# LOAD ROUTES
# -----------------------------

route_query = """
SELECT DISTINCT route_id
FROM operational_record
ORDER BY route_id
"""

routes_df = pd.read_sql(route_query, engine)

route_list = routes_df["route_id"].tolist()

# -----------------------------
# USER INPUTS
# -----------------------------

route_id = st.selectbox(
    "Select Route",
    route_list
)

vehicle_age = st.number_input(
    "Vehicle Age (Years)",
    min_value=0,
    max_value=30,
    value=5
)

# -----------------------------
# AUTO DISTANCE CALCULATION
# -----------------------------

distance_query = f"""
SELECT AVG(total_distance) AS avg_distance
FROM operational_record
WHERE route_id = {route_id}
"""

distance_df = pd.read_sql(distance_query, engine)

avg_distance = round(
    distance_df["avg_distance"][0],
    2
)

st.info(f"Average Route Distance: {avg_distance} km")

# -----------------------------
# BENCHMARK LOGIC
# -----------------------------

operation_type = st.selectbox(
    "Operation Type",
    ["In-City", "Outside-City"]
)

if operation_type == "In-City":
    benchmark = 90
else:
    benchmark = 102
# -----------------------------
# PREDICTION
# -----------------------------

if st.button("Predict Fuel Requirement"):

    # -----------------------------
    # PREPARE INPUT DATA
    # -----------------------------

    input_data = pd.DataFrame({
    "route_id": [route_id],
    "total_distance": [avg_distance],
    "vehicle_age": [vehicle_age]
})

    # -----------------------------
    # MAKE PREDICTION
    # -----------------------------

    prediction = model.predict(input_data)

    fuel_required = prediction[0]

    # -----------------------------
    # SHOW PREDICTION
    # -----------------------------

    st.subheader("Predicted Fuel Requirement")

    st.success(
        f"Estimated Efficient Fuel Allocation: "
        f"{fuel_required:.2f} Liters"
    )

    # -----------------------------
    # BENCHMARK COMPARISON
    # -----------------------------

    difference = fuel_required - benchmark

    st.subheader("DSS Interpretation")

    st.write(f"Operational Benchmark: {benchmark:.2f} Liters")

    st.write(f"Difference from Benchmark: {difference:.2f} Liters")

    # -----------------------------
    # PERFORMANCE EVALUATION
    # -----------------------------

    if fuel_required <= benchmark:
        performance = "Efficient"

    elif fuel_required <= benchmark + 10:
        performance = "Moderate"

    else:
        performance = "Poor"

    st.metric(
        "Performance Status",
        performance
    )

    # -----------------------------
    # ALERT SYSTEM
    # -----------------------------

    if fuel_required > benchmark + 10:

        st.error(
            "ALERT: Fuel requirement exceeds operational benchmark."
        )

    elif fuel_required < benchmark - 15:

        st.warning(
            "ALERT: Fuel usage unusually below benchmark."
        )

    else:

        st.success(
            "Fuel requirement is within normal operational range."
        )

    # -----------------------------
    # OPERATIONAL RECOMMENDATION
    # -----------------------------

    if performance == "Efficient":

        recommendation = (
            "Vehicle operation is within expected efficiency range. "
            "Fuel allocation can be approved."
        )

    elif performance == "Moderate":

        recommendation = (
            "Fuel consumption is slightly above normal levels. "
            "Monitor vehicle and route performance."
        )

    else:

        if vehicle_age >= 10:

            recommendation = (
                "High fuel requirement detected. "
                "Preventive maintenance and vehicle inspection are recommended."
            )

        else:

            recommendation = (
                "Fuel requirement exceeds operational benchmark. "
                "Review route operational conditions."
            )

    st.subheader("Operational Recommendation")

    st.info(recommendation)
