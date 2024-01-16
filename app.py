import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Updated cache command

@st.cache_resource
def load_data():
    # Load your dataset here
    data = pd.read_csv('Cleaned_Car_sale_ads3.csv')
    # Data cleaning and preprocessing steps
    return data

df = load_data()

st.title('Vehicle Offers Dashboard')
st.write('This dashboard provides insights into vehicle offers.')

# filters
brand = st.sidebar.multiselect('Select Brand', df['Vehicle_brand'].unique())

if brand:
    # If a brand is selected, filter the models accordingly
    filtered_models = df[df['Vehicle_brand'].isin(brand)]['Vehicle_model'].unique()
else:
    # If no brand is selected, display all models
    filtered_models = df['Vehicle_model'].unique()
     
model = st.sidebar.multiselect('Select Model', filtered_models)
# Check if exactly one brand is selected
if len(brand) == 1:
    st.write(f"Model Distribution for Brand: {brand[0]}")

    # Filter the DataFrame for the selected brand
    brand_df = df[df['Vehicle_brand'] == brand[0]]

    # Count the number of each model
    model_count = brand_df['Vehicle_model'].value_counts()

    # Plotting
    plt.figure(figsize=(10, 6))
    sns.barplot(x=model_count.index, y=model_count.values)
    plt.xticks(rotation=90)
    plt.xlabel('Vehicle Model')
    plt.ylabel('Count')
    plt.title(f"Model Distribution for {brand[0]}")
    st.pyplot(plt)

# Slider for Production Year
min_year, max_year = int(df['Production_year'].min()), int(df['Production_year'].max())
production_year = st.sidebar.slider('Select Production Year Range', min_year, max_year, (min_year, max_year))

# Slider for Mileage (km)
min_mileage, max_mileage = int(df['Mileage_km'].min()), int(df['Mileage_km'].max())
mileage_km = st.sidebar.slider('Select Mileage (km) Range', min_mileage, max_mileage, (min_mileage, max_mileage))

# Slider for Horse Power
min_hp, max_hp = int(df['Power_HP'].min()), int(df['Power_HP'].max())
power_hp = st.sidebar.slider('Select Power (HP) Range', min_hp, max_hp, (min_hp, max_hp))
transmission = st.sidebar.multiselect('Select Transmission Type', df['Transmission'].unique())
drive = st.sidebar.multiselect('Select Drive System', df['Drive'].unique())

# Slider for Displacement (cm3)
min_cc, max_cc = int(df['Displacement_cm3'].min()), int(df['Displacement_cm3'].max())
displacement_cm3 = st.sidebar.slider('Select Displacement (cm³)', min_cc, max_cc, (min_cc, max_cc))
# Doors Number
doors_number = st.sidebar.multiselect('Select Number of Doors', df['Doors_number'].unique())

price_column = 'Price'  
# Slider for Price
min_price, max_price = int(df[price_column].min()), int(df[price_column].max())
price_usd = st.sidebar.slider('Select Price (PLN) Range', min_price, max_price, (min_price, max_price))

# Apply filters
filtered_data = df
if brand:
    filtered_data = filtered_data[filtered_data['Vehicle_brand'].isin(brand)]
if model:
    filtered_data = filtered_data[filtered_data['Vehicle_model'].isin(model)]
if transmission:
    filtered_data = filtered_data[filtered_data['Transmission'].isin(transmission)]
if drive:
    filtered_data = filtered_data[filtered_data['Drive'].isin(drive)]
filtered_data = filtered_data[(filtered_data['Production_year'] >= production_year[0]) & (filtered_data['Production_year'] <= production_year[1])]
filtered_data = filtered_data[(filtered_data['Mileage_km'] >= mileage_km[0]) & (filtered_data['Mileage_km'] <= mileage_km[1])]
filtered_data = filtered_data[(filtered_data['Power_HP'] >= power_hp[0]) & (filtered_data['Power_HP'] <= power_hp[1])]
filtered_data = filtered_data[(filtered_data['Displacement_cm3'] >= displacement_cm3[0]) & (filtered_data['Displacement_cm3'] <= displacement_cm3[1])]
if doors_number:
    filtered_data = filtered_data[filtered_data['Doors_number'].isin(doors_number)]
filtered_data = filtered_data[(filtered_data[price_column] >= price_usd[0]) & (filtered_data[price_column] <= price_usd[1])]


# Price Distribution Plot
st.header('Price Distribution')
fig, ax = plt.subplots()
sns.histplot(filtered_data[price_column], ax=ax)
st.pyplot(fig)

# Correlation Heatmap
st.header('Correlation Heatmap')
columns_to_include = ['Production_year', 'Mileage_km', 'Power_HP', 'Displacement_cm3', 'Doors_number', price_column]
corr = filtered_data[columns_to_include].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, fmt=".2f")
st.pyplot(fig)


# Data Table
st.header('Data Table')
st.write(filtered_data)
