# Import Librariries
import streamlit as st
import pandas as pd
import numpy as np
import hydralit_components as hc
import requests
import inspect
from streamlit_lottie import st_lottie
from numerize import numerize
from itertools import chain
import plotly.graph_objects as go
import plotly.express as px
import joblib
import statsmodels.api as sm
import sklearn
from PIL import Image
import matplotlib.pyplot as plt
import os
import seaborn as sns

data_ha = pd.read_csv("diabetes_data.csv")

# Set Page Icon,Title, and Layout
st.set_page_config(layout="wide",  page_title = "Diabetes Disease")
# Load css style file from local disk
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
# Load css style from url
def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',unsafe_allow_html = True)

# Display lottie animations
def load_lottieurl(url):
    # get the url
    r = requests.get(url)
    # if error 200 raised return Nothing
    if r.status_code !=200:
        return None
    return r.json()

# Navigation Bar Design
menu_data = [
{'label':"Overview", 'icon': "bi bi-house"},
{'label':"Data Exploration and Visualization", 'icon': "bi bi-clipboard-data"},
{'label':'Conclusion', 'icon' : "bi bi-graph-up-arrow"}]

# Set the Navigation Bar
menu_id = hc.nav_bar(menu_definition = menu_data,
                    sticky_mode = 'sticky',
                    sticky_nav = False,
                    hide_streamlit_markers = False,
                    override_theme = {'txc_inactive': 'black',
                                        'menu_background' : '#0178e4',
                                        'txc_active':'##808080',
                                        'option_active':'white'})
# Home Page
if menu_id == "Overview":
    st.markdown("<hr style='border-top: 3px solid grey;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Diabetes Disease <i class='bi bi-heart-fill' style='color: red;'></i> Exploration</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 3px solid grey;'>", unsafe_allow_html=True)
   
 # Display Introduction
    st.markdown("<h3 style='text-align: center; color: black;'>Healthcare Analytics Project</h4>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: black;'>Presented by Georges El Hajal to Dr. Samar El Hage</h4>", unsafe_allow_html=True)
    st.markdown(" ")
    st.markdown(" ")

# Splitting page into 2 columns
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")

        st.markdown("<p style='text-align: center; color: black;'>Diabetes is a complex chronic disease that affects the way your body regulates blood glucose (sugar) levels. It occurs when the body either does not produce enough insulin or does not effectively use the insulin it produces. Insulin is a hormone produced by the pancreas that helps regulate the amount of glucose in your bloodstream and allows it to enter your cells, where it is used for energy.Untreated or poorly managed diabetes can lead to high blood glucose levels, which can cause various complications affecting different parts of the body. These complications may include cardiovascular diseases, nerve damage (neuropathy), kidney damage (nephropathy), eye damage (retinopathy), foot problems, and an increased risk of infections.</p>", unsafe_allow_html=True)
    with col2:
        image = Image.open("/Users/georgeshajal/Desktop/MSBA 350/Project Healthcare/glucose_blood.png")
        st.image(image, width=400)

    with col1:
       st.markdown(" ")
       st.markdown(" ")
       st.markdown(" ")
       st.markdown(" ")

       image = Image.open("diabetes_prevention.png")
       st.image(image, width=400)

    with col2:
       st.markdown(" ")
       st.markdown(" ")
       st.markdown(" ")
       st.markdown(" ")
       st.markdown("<p style='text-align: center; color: black;'>The main factors that can possibly lead to diabetes are: unhealthy diet, physical activity, family history and genetics, obesity, smoking as well as others. In this research, we are going to explore which of those factors are mostly related with positive diabetes cases.</p>", unsafe_allow_html=True)
    
  
    st.markdown("<hr style='border-top: 3px solid grey;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: black;'>Upload the Dataset</h4>", unsafe_allow_html=True)

    file = st.file_uploader("Upload CSV file", type="csv")
    if file is not None:
    # Read the CSV file
      data_ha = pd.read_csv("/Users/georgeshajal/Desktop/MSBA 350/Project Healthcare/diabetes_data.csv")
    # Display the DataFrame
      st.dataframe(data_ha.head())
    else: print('Upload your data')

if menu_id == "Data Exploration and Visualization":
    col1, col2, col3 = st.columns([3, 3, 3])
    nb_males = len(data_ha[data_ha["Sex"] == "1"])
    nb_females = len(data_ha[data_ha["Sex"] == "0"])

    with col1:
        theme = {'bgcolor': '#FFFFFF', 'content_color': 'darkgrey', 'progress_color': 'darkgrey'}
        hc.info_card(title="Observations: 70,692", bar_value=70000, theme_override=theme)
    with col2:
        hc.info_card(title="Number of Male:  32,306", bar_value="number_of_males", theme_override=theme)            
    with col3:
        hc.info_card(title="Number of Female: 38,386", bar_value="number_of_females", theme_override=theme)

    with col1:
  
        proportions = data_ha['Sex'].value_counts(normalize=True) * 100
    
        fig = go.Figure(data=[go.Pie(labels=['Female', 'Male'], values=proportions, 
                             hoverinfo='label+percent', textinfo='value+percent', 
                             textfont=dict(size=12), hole=0.4)])

        fig.update_layout(title='Gender Proportions')

        st.plotly_chart(fig)
    with col2:
        # Calculate the percentage of females with diabetes
        total_females = len(data_ha[data_ha['Sex'] == 0])
        females_with_diabetes = len(data_ha[(data_ha['Sex'] == 0) & (data_ha['Diabetes'] == 1)])
        percentage_females_diabetes = (females_with_diabetes / total_females) * 100

# Calculate the percentage of males with diabetes
        total_males = len(data_ha[data_ha['Sex'] == 1])
        males_with_diabetes = len(data_ha[(data_ha['Sex'] == 1) & (data_ha['Diabetes'] == 1)])
        percentage_males_diabetes = (males_with_diabetes / total_males) * 100

        # Create a pie chart using Plotly
        labels = ['Female', 'Male']
        proportions = [percentage_females_diabetes, percentage_males_diabetes]
        fig = go.Figure(data=[go.Pie(labels=labels, values=proportions, 
                             hoverinfo='label+percent', textinfo='value+percent', 
                             textfont=dict(size=12), hole=0.4)])

        fig.update_layout(title='Diabetes Proportions by Gender')
        st.plotly_chart(fig)

    with col3:

        grouped_data = data_ha[data_ha['Diabetes'] == 1].groupby('Age').size().reset_index(name='count')

        fig = px.bar(grouped_data, x='Age', y='count', labels={'age_group': 'Age Group', 'count': 'Number of Positive Diabetes Cases'},
        title='Diabetes Cases per Age Group')

        st.plotly_chart(fig)

    with col1:
        # Filter individuals with BMI < 30, diabetes positive
        filtered_data_below_40 = data_ha[(data_ha['BMI'] < 30) & (data_ha['Diabetes'] == 1)]

# Filter individuals with BMI > 30, diabetes positive
        filtered_data_above_40 = data_ha[(data_ha['BMI'] >= 30) & (data_ha['Diabetes'] == 1)]

        labels = ['BMI < 30', 'BMI >= 30']
        values = [len(filtered_data_below_40), len(filtered_data_above_40)]

        fig = go.Figure(data=[go.Bar(x=labels, y=values)])

# Customize the layout
        fig.update_layout(
        xaxis_title='BMI Category',
        yaxis_title='Number of Individuals with Diabetes',
        title='Individuals with Positive Diabetes by BMI Category'
        )   
        st.plotly_chart(fig)

    with col2:

        total_smokers = len(data_ha[data_ha['Smoker'] == 1])
        smokers_with_diabetes = len(data_ha[(data_ha['Smoker'] == 1) & (data_ha['Diabetes'] == 1)])
        proportion_smokers_diabetes = (smokers_with_diabetes / total_smokers) * 100

# Calculate the proportion of non-smokers with diabetes
        total_non_smokers = len(data_ha[data_ha['Smoker'] == 0])
        non_smokers_with_diabetes = len(data_ha[(data_ha['Smoker'] == 0) & (data_ha['Diabetes'] == 1)])
        proportion_non_smokers_diabetes = (non_smokers_with_diabetes / total_non_smokers) * 100

# Create a pie chart using Plotly
        labels = ['Smokers', 'Non-Smokers']
        proportions = [proportion_smokers_diabetes, proportion_non_smokers_diabetes]

        fig = go.Figure(data=[go.Pie(labels=labels, values=proportions)])

# Customize the layout
        fig.update_layout(title='Proportions of Individuals with Diabetes',
                  annotations=[dict(text=f'{proportion_smokers_diabetes:.2f}%', x=0.18, y=0.5, font_size=20),
                               dict(text=f'{proportion_non_smokers_diabetes:.2f}%', x=0.82, y=0.5, font_size=20)])

# Display the pie chart using Streamlit
        st.plotly_chart(fig)

    with col1:
        phys_activity_1_diabetes_1 = len(data_ha[(data_ha['PhysActivity'] == 1) & (data_ha['Diabetes'] == 1)])
        total_diabetes = len(data_ha[data_ha['Diabetes'] == 1])
        proportion_phys_activity_1_diabetes_1 = (phys_activity_1_diabetes_1 / total_diabetes) * 100

        phys_activity_0_diabetes_1 = len(data_ha[(data_ha['PhysActivity'] == 0) & (data_ha['Diabetes'] == 1)])
        proportion_phys_activity_0_diabetes_1 = (phys_activity_0_diabetes_1 / total_diabetes) * 100

        labels = ['Phys. Activity = 1', 'Phys. Activity = 0']
        proportions = [proportion_phys_activity_1_diabetes_1, proportion_phys_activity_0_diabetes_1]

        fig = go.Figure(data=[go.Pie(labels=labels, values=proportions)])

        fig.update_layout(title='Proportions of Individuals with Diabetes and Physical Activity',
                  annotations=[dict(text=f'{proportion_phys_activity_1_diabetes_1:.2f}%', x=0.25, y=0.5, font_size=20),
                               dict(text=f'{proportion_phys_activity_0_diabetes_1:.2f}%', x=0.75, y=0.5, font_size=20)])

        st.plotly_chart(fig)

    with col2:
        normal_veggies = data_ha[(data_ha['Veggies'] == 1) & (data_ha['Diabetes'] == 1)]

        low_veggies = data_ha[(data_ha['Veggies'] == 0) & (data_ha['Diabetes'] == 1)]

        # Count the occurrences
        count_normal_veggies = len(normal_veggies)
        count_low_veggies = len(low_veggies)

        # Create a bar chart using Plotly
        labels = ['Lots of Veggies', 'Less Veggies']
        values = [count_normal_veggies, count_low_veggies]

        fig = go.Figure(data=[go.Bar(x=labels, y=values)])

        fig.update_layout(
            xaxis_title='Veggies Consumption',
            yaxis_title='Count',
            title='Count of People with Diabetes by Veggies Consumption'
        )

        # Display the bar chart using Streamlit
        st.plotly_chart(fig)

    with col3:
        image = Image.open("diabetes_test.png")
        st.image(image, width=400)

if menu_id == "Conclusion": 
    st.markdown("<hr style='border-top: 3px solid grey;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: black;'>Conclusion <i class='bi bi-heart-fill' style='color: red;'></i> and Recommendations</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border-top: 3px solid grey;'>", unsafe_allow_html=True)   # Splitting page into 2 columns
    col1, col2,col3 = st.columns([3,3,3])
    with col1:
        image = Image.open("/conclusion.png")
    # Display the image in the dashboard
        st.image(image,width=400)   
    with col2:

        st.markdown("<div style='text-align: justify'><h3><b>By using different types of data visualization techniques "
                    "and comparing between the different main causes that trigger diabetes mentioned at the beginning, "
                    "we can notice that individuals clear of those triggering causes have a lower chance of getting diagnosed with diabetes. "
                    "Therefore, we recommend individuals, and especially males aged between 50 and 70 years old to eat a lot of veggies, maintain a good body weight, stay away from smoking and keep a healthy highly active routine.</b></h3></div>",
                    unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown(" ")

    with col3:
        image = Image.open("diabetes_vegg.png")
    # Display the image in the dashboard
        st.image(image)