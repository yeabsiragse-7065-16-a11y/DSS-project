import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from io import BytesIO

engine = create_engine(
    "postgresql://postgres:1234@localhost/fuel_dss"
)
st.title("Operational Reports")

st.write(
    "Generate fuel management reports for a selected period."
)

#Date Range Inputs
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start Date"
    )

with col2:
    end_date = st.date_input(
        "End Date"
    )

if st.button("Generate Report"):
    query = f"""
    SELECT *
    FROM operational_record
    WHERE DATE(operational_date)
    BETWEEN '{start_date}'
    AND '{end_date}'
    """
    df = pd.read_sql(query, engine)
    query = f"""
    SELECT *
    FROM fuel_record
    WHERE DATE(refuel_date)
    BETWEEN '{start_date}'
    AND '{end_date}'
    """
    refuel_df = pd.read_sql(query, engine)
    
    if df.empty:

        st.warning(
        "No records found for selected period."
    )

    else:
        total_distance = df["total_distance"].sum()
        total_trips = df["trip_count"].sum()
        avg_efficiency = df["fuel_efficiency"].mean()    
        total_fuel = refuel_df["refuel_liter"].sum()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
            "Fuel Consumed",
            f"{total_fuel:,.0f} L"
        )

        with col2:
            st.metric(
            "Distance",
            f"{total_distance:,.0f} km"
        )

        with col3:
            st.metric(
            "Trips",
            f"{total_trips:,.0f}"
        )

        with col4:
            st.metric(
            "Avg Efficiency",
            f"{avg_efficiency:.2f} km/L"
        )
    #Vehicle Ranking Report
        vehicle_report = (
        df.groupby("vehicle_id")
        .agg({
          "fuel_efficiency":"mean",
          "total_distance":"sum",
          "trip_count":"sum"
        })
         .reset_index()
        )
        vehicle_report = vehicle_report.sort_values(
        by="fuel_efficiency",
        ascending=False
        )
        st.subheader("Vehicle Performance Ranking")

        st.dataframe(
        vehicle_report,
        use_container_width=True
        )
#Route Ranking Report
        route_report = (
            df.groupby("route_id")
            .agg({
            "fuel_efficiency":"mean",
            "total_distance":"sum"
            })
            .reset_index()
        )
        route_report = route_report.sort_values(
            by="fuel_efficiency",
            ascending=False
        )
        st.subheader("Route Performance Ranking")

        st.dataframe(
        route_report,
        use_container_width=True
    )
#Alert Summary
        alerts_df = df[
            df["fuel_efficiency"] < 2.5
        ]
        st.subheader("Alert Summary")
        st.metric(
        "Vehicles Requiring Attention",
        alerts_df["vehicle_id"].nunique()
        )
        st.dataframe(
        alerts_df[
            [
                "vehicle_id",
                "route_id",
                "fuel_efficiency"
            ]
        ]
    )

        st.write("Vehicle Records:", len(vehicle_report))
        st.write("Route Records:", len(route_report))
        st.write("Alert Records:", len(alerts_df))
# ---------------------------------
# EXCEL EXPORT
# ---------------------------------
        summary_df = pd.DataFrame({
        "Metric": [
        "Total Fuel Consumed",
        "Total Distance",
        "Total Trips",
        "Average Fuel Efficiency"
    ],
        "Value": [
        total_fuel,
        total_distance,
        total_trips,
        round(avg_efficiency, 2)
    ]
})
        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:
            
            vehicle_report.to_excel(
            writer,
            sheet_name="Vehicles",
            index=False
        )
            route_report.to_excel(
            writer,
            sheet_name="Routes",
            index=False
        )

            alerts_df.to_excel(
            writer,
            sheet_name="Alerts",
            index=False
        )

# Move outside the writer block
        excel_data = output.getvalue()

        st.download_button(
        label="Download Excel Report",
        data=excel_data,
        file_name="fuel_management_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )