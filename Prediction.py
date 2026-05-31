import streamlit as st
import pandas as pd
import joblib
from sqlalchemy import create_engine
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"}
    )
else:
    engine = create_engine(
        "postgresql://postgres:1234@localhost:5432/fuel_dss"
    )

# -----------------------------
# LOAD MODEL
# -----------------------------

model = joblib.load("fuel_prediction_model.pkl")
st.markdown("""
<style>

.kpi-card {
    background-color: #ffffff;
    padding: 45px;
    border-radius: 15px;
    border-left: 6px solid #ADD8E6;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    text-align: left;
    margin-bottom: 20px;
}

                      
</style>
""", unsafe_allow_html=True)

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
col1, col2, col3= st.columns([0.5,0.5,2])
with col1:

    route_id = st.selectbox(
        "Select Route",
        route_list
        )
with col2:
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
with col1:   
    st.info(f"Average Route Distance: {avg_distance} km")

# -----------------------------
# BENCHMARK LOGIC
# -----------------------------
with col2:
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
# -----------------------------
# SESSION STATE
# -----------------------------

if "fuel_required" not in st.session_state:

    st.session_state.fuel_required = None
    st.session_state.difference = None
    st.session_state.performance = ""
    st.session_state.comment = ""
    st.session_state.recommendation = ""

# -----------------------------
# PREDICTION
# -----------------------------

if st.button("Predict Fuel Requirement"):

    input_data = pd.DataFrame({

        "route_id": [route_id],
        "total_distance": [avg_distance],
        "vehicle_age": [vehicle_age]

    })

    prediction = model.predict(input_data)

    fuel_required = float(prediction[0])

    difference = fuel_required - benchmark

    # -----------------------------
    # PERFORMANCE EVALUATION
    # -----------------------------

    if fuel_required <= benchmark:

        performance = "Efficient"

    elif fuel_required <= benchmark + 10:

        performance = "Moderate"

    else:

        performance = "Poor"

    # -----------------------------
    # ALERT SYSTEM
    # -----------------------------

    if fuel_required > benchmark + 10:

        comment = (
            "ALERT: Fuel requirement exceeds operational benchmark."
        )

    elif fuel_required < benchmark - 15:

        comment = (
            "ALERT: Fuel usage unusually below benchmark."
        )

    else:

        comment = (
            "Fuel requirement is within normal operational range."
        )

    # -----------------------------
    # RECOMMENDATION ENGINE
    # -----------------------------

    if performance == "Efficient":

        recommendation = (
            "Fuel allocation can be approved."
        )

    elif performance == "Moderate":

        recommendation = (
            "Monitor vehicle and route performance."
        )

    else:

        if vehicle_age >= 10:

            recommendation = (
                "Preventive maintenance and vehicle inspection are recommended."
            )

        else:

            recommendation = (
                "Review route operational conditions."
            )

    # -----------------------------
    # STORE RESULTS
    # -----------------------------

    st.session_state.fuel_required = fuel_required
    st.session_state.difference = difference
    st.session_state.performance = performance
    st.session_state.comment = comment
    st.session_state.recommendation = recommendation

# -----------------------------
# RESULTS PANEL
# -----------------------------

with col3:

    if st.session_state.fuel_required is not None:

        st.markdown(f"""
        <div class="kpi-card">

        <h3>Result</h3>

        <ul>

        <li>
        <b>Estimated Efficient Fuel Allocation:</b>
        {st.session_state.fuel_required:.2f} Liters
        </li>

        <li>
        <b>Operational Benchmark:</b>
        {benchmark:.2f} Liters
        </li>

        <li>
        <b>Difference from Benchmark:</b>
        {st.session_state.difference:.2f} Liters
        </li>

        <li>
        <b>Alert Status:</b>
        {st.session_state.comment}
        </li>

        <li>
        <b>Performance Status:</b>
        {st.session_state.performance}
        </li>

        <li>
        <b>Recommendation:</b>
        {st.session_state.recommendation}
        </li>

        </ul>

        </div>
        """, unsafe_allow_html=True)

     