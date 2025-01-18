import streamlit as st
import pandas as pd
import altair as alt

# Load data
file_path = 'crime_dataset_india.csv'
data = pd.read_csv(file_path)

# Streamlit App Title
st.title("Indian Crimes Statistics Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

# Filter by City
cities = st.sidebar.multiselect(
    "Select City/Cities:", options=data["City"].unique(), default=data["City"].unique()
)

# Filter by Crime Description
crime_descriptions = st.sidebar.multiselect(
    "Select Crime Type(s):", 
    options=data["Crime Description"].unique(), 
    default=data["Crime Description"].unique()
)

# Filter by Victim Gender
genders = st.sidebar.multiselect(
    "Select Victim Gender(s):", 
    options=data["Victim Gender"].unique(), 
    default=data["Victim Gender"].unique()
)

# Filter Data
filtered_data = data[
    (data["City"].isin(cities)) &
    (data["Crime Description"].isin(crime_descriptions)) &
    (data["Victim Gender"].isin(genders))
]

# Overview Statistics
st.header("Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Cases", len(filtered_data))
with col2:
    st.metric("Average Victim Age", f"{filtered_data['Victim Age'].mean():.1f} years")
with col3:
    st.metric("Cases Closed", filtered_data[filtered_data["Case Closed"] == "Yes"].shape[0])

# Data Table
st.subheader("Filtered Data Table")
st.dataframe(filtered_data)

# Visualizations
st.header("Visualizations")

# Crime Counts by City
st.subheader("Crime Counts by City")
city_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X("City", sort="-y"),
    y="count()",
    color="City"
).properties(width=700, height=400)
st.altair_chart(city_chart)

# Victim Age Distribution
st.subheader("Victim Age Distribution")
age_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X("Victim Age", bin=True),
    y="count()",
    color="Victim Gender"
).properties(width=700, height=400)
st.altair_chart(age_chart)

# Crime Domain Breakdown
st.subheader("Crime Domain Breakdown")
domain_data = filtered_data.groupby("Crime Domain")["Report Number"].count().reset_index()
domain_data.rename(columns={"Report Number": "Count"}, inplace=True)
domain_chart = alt.Chart(domain_data).mark_arc().encode(
    theta="Count",
    color="Crime Domain",
    tooltip=["Crime Domain", "Count"]
).properties(width=400, height=400)
st.altair_chart(domain_chart)

# Detailed View for a Selected City
st.header("Detailed City Statistics")
selected_city = st.selectbox("Select a City:", options=filtered_data["City"].unique())
if selected_city:
    city_data = filtered_data[filtered_data["City"] == selected_city]
    st.write(city_data)
