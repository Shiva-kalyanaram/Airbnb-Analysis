import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Airbnb Data Visualization | By Shiva",
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items=None)

# Reading the cleaned DataFrame (replace this with your actual data)
df = pd.read_csv('Airbnb_data.csv')

# Sidebar for user input
st.title('Airbnb Data Analysis and visualization')
st.sidebar.header("Explore Data")
country = st.sidebar.selectbox("Select Country", sorted(df['Country'].unique()))
room_type = st.sidebar.selectbox("Select Room Type", sorted(df['Room_type'].unique()))

# Price Analysis inputs
property_type = st.sidebar.selectbox("Select Property Type", sorted(df['Property_type'].unique()))
price_range = st.sidebar.slider('Select Price Range', df['Price'].min(), df['Price'].max(), (df['Price'].min(), df['Price'].max()))

# Main page selection
page_selection = st.radio("Select Page", ["Table View", "Visual View", "Price Analysis"])

# Table View Page
if page_selection == "Table View":
    # Filter the data based on user input
    filtered_df = df[(df['Country'] == country) & (df['Room_type'] == room_type)]

    # Display the top 10 hosts with the highest number of listings
    st.header("Top 10 Hosts with Highest Number of Listings")
    top_hosts = filtered_df.groupby("Host_name").size().nlargest(10).reset_index(name="Listings")
    st.table(top_hosts)

    # Display total listings in each room type
    st.header("Total Listings in Each Room Type")
    total_listings_by_room_type = filtered_df.groupby("Room_type").size().reset_index(name="Total_Listings")
    st.table(total_listings_by_room_type)

    # Display top 10 property types available
    st.header("Top 10 Property Types Available")
    top_property_types = df.groupby("Property_type").size().nlargest(10).reset_index(name="Listings")
    st.table(top_property_types)

# Visual View Page
elif page_selection == "Visual View":
    st.title("Visual Representations")

    # Query 1: Top 10 Property Types available
    if st.checkbox("Show Top 10 Property Types available"):
        st.header("Top 10 Property Types available")
        fig1, ax1 = plt.subplots(figsize=(10, 8))
        ax1 = sns.countplot(data=df, y=df.Property_type.values, order=df.Property_type.value_counts().index[:10])
        ax1.set_title("Top 10 Property Types available")
        st.pyplot(fig1)

    # Query 2: Total Listings in each Room Type
    if st.checkbox("Show Total Listings in each Room Type"):
        st.header("Total Listings in each Room Type")
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        ax2 = sns.countplot(data=df, x=df.Room_type)
        ax2.set_title("Total Listings in each Room Type")
        st.pyplot(fig2)

    # Query 3: Top 10 Hosts with Highest number of Listings
    if st.checkbox("Show Top 10 Hosts with Highest number of Listings"):
        st.header("Top 10 Hosts with Highest number of Listings")
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        ax3 = sns.countplot(data=df, y=df.Host_name, order=df.Host_name.value_counts().index[:10])
        ax3.set_title("Top 10 Hosts with Highest number of Listings")
        st.pyplot(fig3)

    # Query 4: Choropleth Map
    if st.checkbox("Show Choropleth Map"):
        st.header("Choropleth Map")
        fig4 = px.choropleth(data_frame=df, locations='Country_code', color='Country', locationmode='country names')
        st.plotly_chart(fig4)

    # Query 5: Scatter Plot - Avg Listing Price in each Country
    if st.checkbox("Show Scatter Plot - Avg Listing Price in each Country"):
        st.header("Scatter Plot - Avg Listing Price in each Country")
        country_df = df.groupby('Country', as_index=False)['Price'].mean()
        fig5 = px.scatter(data_frame=country_df, x='Country', y='Price', color='Country', size='Price',
                          opacity=1, size_max=35, title='Avg Listing Price in each Countries')
        st.plotly_chart(fig5)

    # Query 6: Bar Plot - Avg Review Scores by Room Type
    if st.checkbox("Show Bar Plot - Avg Review Scores by Room Type"):
        st.header("Bar Plot - Avg Review Scores by Room Type")
        rev_df = df.groupby('Room_type', as_index=False)['Review_scores'].mean().sort_values(by='Review_scores')
        fig6 = px.bar(data_frame=rev_df, x='Room_type', y='Review_scores', color='Review_scores')
        st.plotly_chart(fig6)

    # Query 7: Bar Plot - Avg Price by Room Type
    if st.checkbox("Show Bar Plot - Avg Price by Room Type"):
        st.header("Bar Plot - Avg Price by Room Type")
        pr_df = df.groupby('Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
        fig7 = px.bar(data_frame=pr_df, x='Room_type', y='Price', color='Price')
        st.plotly_chart(fig7)

# Price Analysis Page
elif page_selection == "Price Analysis":
    st.markdown("## Price Analysis")

    # CREATING COLUMNS
    col1, col2 = st.columns(2, gap='medium')

    with col1:
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(f'Country == "{country}" & Room_type == "{room_type}" & Property_type == "{property_type}" & Price >= {price_range[0]} & Price <= {price_range[1]}').groupby('Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type'
                     )
        st.plotly_chart(fig, use_container_width=True)

        # HEADING 2
        st.markdown("## Availability Analysis")

        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(f'Country == "{country}" & Room_type == "{room_type}" & Property_type == "{property_type}" & Price >= {price_range[0]} & Price <= {price_range[1]}'),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                     )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(f'Country == "{country}" & Room_type == "{room_type}" & Property_type == "{property_type}" & Price >= {price_range[0]} & Price <= {price_range[1]}').groupby('Country', as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                             locations='Country',
                             color='Price',
                             hover_data=['Price'],
                             locationmode='country names',
                             size='Price',
                             title='Avg Price in each Country',
                             color_continuous_scale='agsunset'
                             )
        col2.plotly_chart(fig, use_container_width=True)

        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")

        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(f'Country == "{country}" & Room_type == "{room_type}" & Property_type == "{property_type}" & Price >= {price_range[0]} & Price <= {price_range[1]}').groupby('Country', as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                             locations='Country',
                             color='Availability_365',
                             hover_data=['Availability_365'],
                             locationmode='country names',
                             size='Availability_365',
                             title='Avg Availability in each Country',
                             color_continuous_scale='agsunset'
                             )
        st.plotly_chart(fig, use_container_width=True)
