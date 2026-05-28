import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -----------------------------
# DATABASE CONNECTION
# -----------------------------

DATABASE_URL = "postgresql://postgres:1234@localhost/fuel_dss"

engine = create_engine(DATABASE_URL)

# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("Fuel Usage Alerts")

st.write(
    "Anomaly detection and operational alerts."
)

# -----------------------------
# LOAD DATA
# -----------------------------

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

# -----------------------------
# DEFINE BENCHMARKS
# -----------------------------

EFFICIENCY_THRESHOLD_LOW = 1.5
EFFICIENCY_THRESHOLD_HIGH = 5.0

OLD_VEHICLE_AGE = 10

# -----------------------------
# DETECT ALERTS
# -----------------------------

high_consumption = df[
    df["fuel_efficiency"] < EFFICIENCY_THRESHOLD_LOW
]

excellent_efficiency = df[
    df["fuel_efficiency"] > EFFICIENCY_THRESHOLD_HIGH
]

old_vehicle_alert = df[
    (df["vehicle_age"] >= OLD_VEHICLE_AGE)
    &
    (df["fuel_efficiency"] < 2)
]

# -----------------------------
# KPI SUMMARY
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "High Consumption Alerts",
        len(high_consumption)
    )

with col2:

    st.metric(
        "Excellent Efficiency Records",
        len(excellent_efficiency)
    )

with col3:

    st.metric(
        "Old Vehicle Risk Alerts",
        len(old_vehicle_alert)
    )

# -----------------------------
# HIGH CONSUMPTION ALERTS
# -----------------------------

st.subheader("High Fuel Consumption Vehicles")

if len(high_consumption) > 0:

    st.error(
        "Vehicles operating below efficiency threshold detected."
    )

    st.dataframe(
        high_consumption[
            [
                "vehicle_id",
                "route_id",
                "fuel_efficiency",
                "vehicle_age"
            ]
        ]
    )

else:

    st.success(
        "No major high-consumption anomalies detected."
    )

# -----------------------------
# OLD VEHICLE ALERTS
# -----------------------------

st.subheader("Old Vehicle Operational Risk")

if len(old_vehicle_alert) > 0:

    st.warning(
        "Older vehicles with poor efficiency detected."
    )

    st.dataframe(
        old_vehicle_alert[
            [
                "vehicle_id",
                "route_id",
                "vehicle_age",
                "fuel_efficiency"
            ]
        ]
    )

else:

    st.success(
        "No old vehicle efficiency risks detected."
    )

# -----------------------------
# EXCELLENT PERFORMANCE
# -----------------------------

st.subheader("Top Efficient Vehicles")

if len(excellent_efficiency) > 0:

    st.success(
        "Highly efficient operational records identified."
    )

    st.dataframe(
        excellent_efficiency[
            [
                "vehicle_id",
                "route_id",
                "fuel_efficiency"
            ]
        ]
    )

# -----------------------------
# DSS RECOMMENDATIONS
# -----------------------------

st.subheader("Operational Recommendations")

if len(high_consumption) > 50:

    st.error(
        """
        Large number of inefficient operations detected.
        Recommend managerial review and maintenance inspection.
        """
    )

elif len(high_consumption) > 20:

    st.warning(
        """
        Moderate abnormal fuel consumption observed.
        Monitor route and vehicle performance closely.
        """
    )

else:

    st.success(
        """
        Fuel usage patterns are generally stable.
        """
    )