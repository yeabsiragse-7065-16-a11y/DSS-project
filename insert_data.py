from sqlalchemy import create_engine
import pandas as pd

# Database connection
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "fuel_dss"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print("Database connected successfully!")
# Load dataset
df = pd.read_excel("data/fuel_dataset.xlsx")

# Standardize column names
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")
#insert vehicle data
print(df.head())
vehicle_df = df[
    [
        'vehicle_id',
        'vehicle_depo',
        'vehicle_model',
        'vehicle_age',
        'fuel_type',
        'maintenance_status'
    ]
].drop_duplicates()

vehicle_df.to_sql(
    'vehicle',
    engine,
    if_exists='append',
    index=False
)

print("Vehicle data inserted!")
#insert route data
route_df = df[['route_id']].drop_duplicates()

route_df.to_sql(
    'route',
    engine,
    if_exists='append',
    index=False
)

print("Route data inserted!")
#insert fuel_record data
fuel_df = df[
    [
        'fuel_cycle_id',
        'vehicle_id',
        'date',
        'refuel_liter',
        'refuel_point'
    ]
].copy()

fuel_df.rename(columns={
    'date': 'refuel_date'
}, inplace=True)

fuel_df.to_sql(
    'fuel_record',
    engine,
    if_exists='append',
    index=False
)

print("Fuel record data inserted!")
#insert operational record data
operational_df = df[
    [
        'vehicle_id',
        'route_id',
        'date',
        'trip_count',
        'total_distance',
        'cycle_period',
        'fuel_efficiency'
    ]
].copy()

operational_df.rename(columns={
    'date': 'operational_date'
}, inplace=True)

operational_df.to_sql(
    'operational_record',
    engine,
    if_exists='append',
    index=False
)

print("Operational data inserted!")