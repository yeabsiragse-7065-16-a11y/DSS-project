import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title("Fuel Efficiency Analytics")

# DATABASE CONNECTION
engine = create_engine(
    "DATABASE_URL"
)

# LOAD DATA
query = """
SELECT
    o.vehicle_id,
    o.route_id,
    o.total_distance,
    o.fuel_efficiency,
    v.vehicle_age
FROM operational_record o
JOIN vehicle v
    ON o.vehicle_id = v.vehicle_id
    WHERE v.vehicle_age IS NOT NULL
"""

df = pd.read_sql(query, engine)

#PERFORMANCE CLASSIFICATION

def classify_performance(efficiency):

    if efficiency >= 4:
        return "Efficient"

    elif efficiency >= 2:
        return "Moderate"

    else:
        return "Poor"

df["performance"] = df[
    "fuel_efficiency"
].apply(classify_performance)

#VEHICLE PERFORMANCE TABLE

vehicle_performance = df.groupby(
    "vehicle_id"
)["fuel_efficiency"].mean().reset_index()

vehicle_performance = vehicle_performance.sort_values(
    by="fuel_efficiency",
    ascending=False
)

st.subheader("Vehicle Performance Ranking")

st.dataframe(vehicle_performance)

#BEST & WORST VEHICLES

best_vehicle = vehicle_performance.iloc[0]

worst_vehicle = vehicle_performance.iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"Best Vehicle: {best_vehicle['vehicle_id']}"
    )

with col2:
    st.error(
        f"Worst Vehicle: {worst_vehicle['vehicle_id']}"
    )

#ROUTE EFFICIENCY ANALYSIS

route_analysis = df.groupby(
    "route_id"
)["fuel_efficiency"].mean().reset_index()

st.subheader("Route Efficiency")

st.bar_chart(
    route_analysis.set_index("route_id")
)

#AGE VS EFFICIENCY


age_analysis = df.groupby(
    "vehicle_age"
)["fuel_efficiency"].mean().reset_index()

st.subheader("Efficiency By Vehicle Age")

st.bar_chart(
    age_analysis.set_index("vehicle_age")
)

#PERFORMANCE DISTRIBUTION

performance_counts = df[
    "performance"
].value_counts()

st.subheader("Performance Categories")

st.bar_chart(performance_counts)

#DSS INSIGHTS

st.subheader("Operational Insights")

avg_efficiency = df[
    "fuel_efficiency"
].mean()

if avg_efficiency < 2:

    st.error(
        "Overall fleet efficiency is below expected levels."
    )

elif avg_efficiency < 4:

    st.warning(
        "Fleet performance is moderate."
    )

else:

    st.success(
        "Fleet efficiency is operating within expected range."
    )
