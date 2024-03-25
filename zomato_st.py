

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from IPython.display import display
import ipywidgets as widgets


import base64

st.set_page_config(layout='wide')
def sidebar_bg(side_bg):
   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file) 
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

sidebar_bg(r"/Users/sathish/Desktop/zomato1.jpeg")
set_png_as_page_bg("/Users/sathish/Desktop/z3.webp")
from streamlit_option_menu import option_menu
with st.sidebar:
    st.title(":white[Contents]")
   
    selected =option_menu( menu_title= "Overview",
          options=["Home","Insights","Explore data"],
          icons=["house-door","graph-up-arrow","bar-chart-line"],
          menu_icon="book-fill",
          default_index=0,styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
         
if selected == "Home":
         # Title Image
    t1,c1,c2,c4=st.columns([1,1,1,11])
    with t1:
        title_html = '''
        <h1 style="text-align: center; color: black;">
            <a  style="text-decoration: none; color: #C70623;">
                ZOMATO DATA ANALYSIS 
            </a>
        
        </h1><br>'''

    st.markdown(title_html, unsafe_allow_html=True)

    col1,col2 = st.columns(2,gap= 'medium')

    with col2:
        st.write("Zomato is an Indian multinational restaurant aggregator and food delivery company. It was founded by Deepinder Goyal and Pankaj Chaddah in 2008. Zomato provides information, menus and user-reviews of restaurants as well as food delivery options from partner restaurants in more than 1,000 Indian cities and towns, as of 2022–23.Zomato rivals Swiggy in food delivery and hyperlocal space.")
        video_file ="https://www.youtube.com/watch?v=xjNnqRngdzs"    

    with col1:
         
         st.video(video_file)
if selected == "Explore data":

    t1,c1,c2,c4=st.columns([1,1,1,11])
    with t1:
        title_html = '''
        <h1 style="text-align: center; color: black;">
            <a  style="text-decoration: none; color: #2CD1D6;">
                ZOMATO DATA ANALYSIS 
            </a>
        
        </h1><br>'''

    st.markdown(title_html, unsafe_allow_html=True)



    df=pd.read_csv('/Users/sathish/Downloads/zomato.csv')

    country_codes_df = pd.read_excel('/Users/sathish/Downloads/Country-Code.xlsx')
    st.title("Zomato Analysis")

    df_merge = pd.merge(df,country_codes_df,on='Country Code',how='left')


    #Let's plot some charts to understand the data better:
    name = df_merge['Country'].value_counts().index #Index function helps us to view only country name, inorder to view the more information about the country do not use index word.
  
    value = df_merge['Country'].value_counts().values
    fig, ax1 = plt.subplots()
    ax1.pie(value[:5], labels=name[:5])
    ax1.set_title('This shows the distribution of all this countries usage of zomato.')
    st.pyplot(fig)

    # Sample data
    currencies = ['Rupees', 'USD', 'Euro', 'Pound', 'Yen','Botswana']  # Assuming these are the currencies
    exchange_rates = [1, 82.81, 90.16, 105.38, 0.55,6.06]  # Sample exchange rates for illustration
    # Create bar chart
    fig, ax = plt.subplots()
    ax.bar(currencies, exchange_rates, color='skyblue')
    ax.set_xlabel('Currencies')
    ax.set_ylabel('Exchange Rates')
    ax.set_title('Exchange Rates for Different Currencies')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Display chart using Streamlit
    st.pyplot(fig)


    countries = country_codes_df['Country Code'].unique()
    countries_names = country_codes_df['Country'].unique()
    city_names=df['City'].unique()


    selected_country = st.selectbox('Select a Country Code', countries_names)
    filtered_df = df[df['Country Code'] == selected_country]

    # Display the selected country code
    st.write('You selected:', selected_country)

    if not filtered_df.empty:
        cuisine_counts = df['Cuisines'].str.split(', ', expand=True).stack().value_counts()
        fig3,ax3=plt.subplots()
        ax3 = px.bar(filtered_df, x=cuisine_counts.index, y=cuisine_counts.values, title=f'Favorite Cuisines in {selected_country}')
        st.pyplot(fig)

    else:
        st.write("No data available for the selected country.")

    #TOP 10 COSTLY CUSINES IN INDIA
        
    indian_restaurants = df[df['Country Code'] == 1]

    # Calculate the average cost for two people dining for each cuisine
    cuisine_avg_cost = indian_restaurants.groupby('Cuisines')['Average Cost for two'].mean().sort_values(ascending=False)

    # Plot the cuisines with the highest average cost using Plotly
    fig = px.bar(x=cuisine_avg_cost.head(10).values, y=cuisine_avg_cost.head(10).index, orientation='h',
                labels={'x': 'Average Cost for Two', 'y': 'Cuisine'}, title='Top 10 Costly Cuisines in India')
    st.plotly_chart(fig)


if selected=="Insights":
    df=pd.read_csv('/Users/sathish/Downloads/zomato.csv')


# Allow the user to select a city
    selected_city = st.selectbox('Select a City', df['City'].unique())

    # Filter the DataFrame based on the selected city
    city_restaurants = df[df['City'] == selected_city]

    # Calculate the popularity of each cuisine in the city
    cuisine_popularity = city_restaurants['Cuisines'].str.split(', ', expand=True).stack().value_counts()

    # Calculate the average cost for two people dining for each cuisine in the city
    cuisine_avg_cost = city_restaurants.groupby('Cuisines')['Average Cost for two'].mean()

    # Find the most popular cuisine in the city
    most_popular_cuisine = cuisine_popularity.idxmax()

    # Find the costliest cuisine in the city
    costliest_cuisine = cuisine_avg_cost.idxmax()

    # Display the results
    st.write('Selected City:', selected_city)
    st.write('Most Popular Cuisine in {} is: {}'.format(selected_city, most_popular_cuisine))
    st.write('Costliest Cuisine in {} is: {}'.format(selected_city, costliest_cuisine))



    # Calculate the rating count in the city based on the rating text
    rating_counts = city_restaurants['Rating text'].value_counts()

    # Plot the rating count in the city
    st.write('Rating Counts in {}:'.format(selected_city))
    st.bar_chart(rating_counts)

    # Create a pie chart showing the distribution of restaurants offering online delivery versus dine-in
    online_delivery_counts = city_restaurants['Has Online delivery'].value_counts()
    dine_in_counts=city_restaurants['Has Table booking'].value_counts()

    fig, ax = plt.subplots()
    ax.pie(online_delivery_counts, labels=online_delivery_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
    ax.set_title('Online Delivery Distribution')

    # Display the pie chart for online delivery
    st.pyplot(fig)

    # Create another Streamlit pie chart
    fig2, ax2 = plt.subplots()
    ax2.pie(dine_in_counts, labels=dine_in_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
    ax2.set_title('Dine-in Distribution')

    # Display the pie chart for dine-in
    st.pyplot(fig2)

    st.set_option('deprecation.showPyplotGlobalUse', False)

    indian_restaurants = df[df['Country Code'] == 1]

    # Calculate the total amount spent on online delivery for each city or region in India
    online_delivery_spending = indian_restaurants.groupby('City')['Average Cost for two'].sum()

    # Visualize the comparison between different cities or regions based on the total amount spent on online delivery
    plt.figure(figsize=(10, 6))
    online_delivery_spending.plot(kind='bar')
    plt.xlabel('City')
    plt.ylabel('Total Amount Spent on Online Delivery')
    plt.title('Comparison of Online Delivery Spending Across Cities in India')

    # Display the plot
    st.pyplot()



    city_restaurants = df[df['City'] == selected_city]

    # Filter the DataFrame for restaurants in India
    indian_restaurants = df[df['Country Code'] == 1]  # Assuming India's country code is 1

    # Calculate the total amount spent on dine-in for each city in India
    dine_in_spending = city_restaurants.groupby('City')['Average Cost for two'].sum()

    # Determine which city spends the most on dine-in
    city_with_max_dine_in_spending = dine_in_spending.idxmax()
    max_dine_in_spending = dine_in_spending.max()

    print("City with the highest spending on dine-in:", city_with_max_dine_in_spending)
    print("Total amount spent on dine-in in this city:", max_dine_in_spending)




    # Filter the DataFrame for restaurants in India
    indian_restaurants = df[df['Country Code'] == 1]  # Assuming India's country code is 1

    # Get unique states in India
    indian_states = indian_restaurants['Locality Verbose'].str.split(', ').str[-2].unique()

    # Allow the user to select a state
    selected_state = st.selectbox('Select a State in India', indian_states)




    # Filter the DataFrame based on the selected state
    state_restaurants = indian_restaurants[indian_restaurants['Locality Verbose'].str.contains(selected_state)]

    # Calculate the total amount spent on dine-in for each city in the selected state
    dine_in_spending = state_restaurants.groupby('City')['Average Cost for two'].sum()

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    dine_in_spending.sort_values(ascending=False).plot(kind='bar', color='skyblue')
    plt.title(f'Total Dine-in Spending by City in {selected_state}')
    plt.xlabel('City')
    plt.ylabel('Total Dine-in Spending')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(plt)
