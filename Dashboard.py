import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from sqlalchemy import create_engine
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    st.error("DATABASE_URL environment variable not set in Render!")
    st.stop()

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
#DATABASE_URL = os.getenv("DATABASE_URL")

#if DATABASE_URL:
  #  engine = create_engine(
  #      DATABASE_URL,
  #      connect_args={"sslmode": "require"}
 #   )
#else:
  #  engine = create_engine(
  #      "postgresql://postgres:1234@localhost:5432/fuel_dss"
 #   )
# LOAD DATA
operational_query = """
SELECT *
FROM operational_record
"""
fuel_query = """
SELECT *
FROM fuel_record
"""

df = pd.read_sql(operational_query, engine)

fuel_df = pd.read_sql(fuel_query, engine)

 
# PAGE TITLE
st.title("Dashboard")
# ---------------------------------
# KPI CARD STYLE
# ---------------------------------

st.markdown("""
<style>

.kpi-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #1f4e79;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 20px;
}

.kpi-title {
    font-size: 18px;
    color: gray;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 32px;
    font-weight: bold;
    color: #1f4e79;
}

.kpi-value1 {
    font-size: 32px;
    font-weight: bold;
    color: #FF0000;
}  

.kpi-value2 {
    font-size: 32px;
    font-weight: bold;
    color: #00FF00;
}                       
</style>
""", unsafe_allow_html=True)

# KPIs
total_vehicle = int(df["vehicle_id"].nunique())

avg_efficiency = round(
    df["fuel_efficiency"].mean(),
    2
)

total_distance = round(
    df["total_distance"].sum(),
    2
)
total_fuel_used = round(
    fuel_df["refuel_liter"].sum(),
    2
)
total_records = len(df)
best_vehicle = (
    df.groupby("vehicle_id")[
        "fuel_efficiency"
    ]
    .mean()
    .idxmax()
)
worst_vehicle = (
    df.groupby("vehicle_id")[
        "fuel_efficiency"
    ]
    .mean()
    .idxmin()
)
best_route = (
    df.groupby("route_id")[
        "fuel_efficiency"
    ]
    .mean()
    .idxmax()
)
worst_route = (
    df.groupby("route_id")[
        "fuel_efficiency"
    ]
    .mean()
    .idxmin()
)
st.set_page_config(layout="wide")
# KPI CARDS 1
col1, col2, col3, col4 = st.columns(4)

with col1:
        st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Operational Records</div>
        <div class="kpi-value">
            {total_records}
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Vehicle</div>
        <div class="kpi-value">
            {total_vehicle}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Distance</div>
        <div class="kpi-value">
            {total_distance}
        </div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Fuel Used (Liters)</div>
        <div class="kpi-value">
            {total_fuel_used}
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")
# KPI CARDS 2

col5, col6, col7 = st.columns(3)

with col5:
        st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Fuel Efficiency</div>
        <div class="kpi-value">
            {avg_efficiency}
        </div>
    </div>
    """, unsafe_allow_html=True)
with col6:
            st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Best Vehicle</div>
        <div class="kpi-value2">
            {best_vehicle}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col7:
            st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Worst Vehicle</div>
        <div class="kpi-value1">
            {worst_vehicle}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
st.markdown("---")
# KPI CARDS 3

col8, col9 = st.columns(2)

with col8:
            st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Efficient Route</div>
        <div class="kpi-value2">
            {best_route}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col9:
            st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Inefficient Route</div>
        <div class="kpi-value1">
            {worst_route}
        </div>
    </div>
    """, unsafe_allow_html=True)
    

st.divider()

# RECENT RECORDS

st.subheader("Recent Operational Records")

st.dataframe(df.head(20))

