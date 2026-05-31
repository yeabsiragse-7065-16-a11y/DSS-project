import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:1234@localhost/fuel_dss"
)
st.markdown("""
<style>
    background: linear-gradient(
        135deg,
        #F8FAFC,
        #EEF5FF
    );
</style>
""", unsafe_allow_html=True)
st.title("Vehicle Performance")
col1, col2, col3 = st.columns(3)

with col1:
    vehicle_id = st.number_input(
    "Enter Vehicle ID",
    min_value=0

)
    
# -----------------------------
# AUTO GENERATED DATA
# -----------------------------

vehicle_query = f"""
SELECT 
    vehicle_model,
    vehicle_age
FROM vehicle
WHERE vehicle_id = {vehicle_id}
"""

vehicle_df = pd.read_sql(vehicle_query, engine)


if not vehicle_df.empty:

    vehicle_model = vehicle_df.iloc[0]["vehicle_model"]
    vehicle_age = vehicle_df.iloc[0]["vehicle_age"]

    with col2:
        st.metric(
            "Vehicle Model",
            vehicle_model
        )

    with col3:
        st.metric(
            "Vehicle Age",
            vehicle_age
        )

else:

    with col2:
        st.metric(
            "Vehicle Model",
            "-"
        )

    with col3:
        st.metric(
            "Vehicle Age",
            "-"
        )
 
if st.button("Analyze Vehicle"):

    query = f"""
    SELECT
        vehicle_id,
        AVG(fuel_efficiency) AS avg_efficiency,
        SUM(total_distance) AS total_distance,
        SUM(trip_count) AS total_trips
    FROM operational_record
    WHERE vehicle_id = {vehicle_id}
    GROUP BY vehicle_id
    """
    df = pd.read_sql(query, engine)
   
    route_query = f"""
    SELECT
        route_id,
        AVG(fuel_efficiency) AS avg_efficiency
    FROM operational_record
    WHERE vehicle_id = {vehicle_id}
    GROUP BY route_id
    ORDER BY avg_efficiency DESC
    """
    route_df = pd.read_sql(route_query, engine)
    
    refuel_query = f"""
  SELECT
        vehicle_id,
        SUM(refuel_liter) AS fuel_used
    FROM fuel_record
    WHERE vehicle_id = {vehicle_id}
    GROUP BY vehicle_id
        """
    refuel_df = pd.read_sql(refuel_query, engine)

    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
 
    if not df.empty:

        efficiency = df["avg_efficiency"][0]
        with col4:
         st.metric(
            "Average Fuel Efficiency",
            f"{efficiency:.2f}"
        )
        with col1:
            st.metric(
            "Total Distance",
            f"{df['total_distance'][0]:,.0f} km"
        )
        with col2:
            st.metric(
            "Total Trips",
            int(df["total_trips"][0])
        )
        with col3:
            st.metric(
            "Total Fuel Consumed",
            f"{refuel_df["fuel_used"][0]:,.0f} L"
        )    
        with col5:
            if not route_df.empty:

                best_route = route_df.iloc[0]["route_id"]
                best_route_efficiency = (
                route_df.iloc[0]["avg_efficiency"]
                )
                st.metric(
                    "Most Efficient Route",
                    int(best_route)
                    )

        with col6:
            if efficiency >= 4:
                st.success(
                "Efficient Vehicle"
            )
            elif efficiency >= 2.5:

                st.warning(
                "Moderate Efficiency"
            )
            else:

                st.error(
                "Poor Efficiency"
            )
    else:

        st.warning(
            "Vehicle not found."
        )
