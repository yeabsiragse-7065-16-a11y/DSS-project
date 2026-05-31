import streamlit as st
import pandas as pd
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
    background-color: white;    
    padding: 15px;
    border-radius: 15px;
    border-left: 6px solid #ADD8E6;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    text-align: center;
    margin-bottom: 15px;
}

.kpi-title {
    font-size: 18px;
    color: black;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 24px;
    font-weight: bold;
    color: #1f4e79;
}
                      
</style>
""", unsafe_allow_html=True)

# KPIs
total_vehicle = int(df["vehicle_id"].nunique())

total_distance = round(
    df["total_distance"].sum(),
    2
)
total_fuel_used = round(
        
    fuel_df["refuel_liter"].sum(),
    2
)
total_records = len(df)

#st.set_page_config(layout="wide")
# KPI CARDS 1
col1, col2, col3, col4 = st.columns(4)

with col1:
        st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Operational Records</div>
        <div class="kpi-value">
            {total_records:,}
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Vehicle</div>
        <div class="kpi-value">
            {total_vehicle:,}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Distance(km)</div>
        <div class="kpi-value">
            {total_distance:,}
        </div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Fuel Used (Liters)</div>
        <div class="kpi-value">
            {total_fuel_used:,}
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")
# KPI CARDS 2
col1, col2= st.columns([1.5,1.5])


# RECENT RECORDS
with col1:
      
        st.header("Recent Operational Records")
        st.dataframe(df.head(20))
with col2:
        trend_query = """
        SELECT
            operational_date,
            AVG(fuel_efficiency) AS avg_efficiency
        FROM operational_record
        GROUP BY operational_date
        ORDER BY operational_date
        """

        trend_df = pd.read_sql(
            trend_query,
            engine
        )

        st.subheader("Fuel Efficiency Trend")
        st.line_chart(
            trend_df.set_index("operational_date")
        )
        

