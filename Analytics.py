import streamlit as st
import pandas as pd

from sqlalchemy import create_engine
from io import BytesIO
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:1234@localhost/fuel_dss"
)
analysis_option = st.radio(
    "Select Analysis Type",
    [
        "Reports",
        "Vehicle Performance"
    ],
    horizontal=True
)


if analysis_option == "Reports":

    # reports code here

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

                st.error(
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


elif analysis_option == "Vehicle Performance":

    # vehicle analysis code here
            
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

                st.error(
                    "Vehicle not found."
                )

















































































































































































