import pandas as pd
import streamlit as st
import plotly.express as px


st.header("Customizable Bubble Plot 🫧")
st.write("Enter your parameters and ranges and plot your Customized Bubble Plot ")
@st.cache_data
def load_data(file_path):
        data = pd.read_csv(file_path, compression='gzip')
        return data

maindata = load_data(r'C:\Users\apala\OneDrive\Documents\PythonScripts\project\Untitled Folder\streamlitstuff\customize_data.csv')

@st.cache_data
def filter_data(data, x_axis, y_axis, age_range=None, year_range=None, rating_range=None):
        filtered_data = data.copy()
        if age_range is not None:
            filtered_data = filtered_data[(filtered_data['age'] >= age_range[0]) & (filtered_data['age'] <= age_range[1])]
        if year_range is not None:
            filtered_data = filtered_data[(filtered_data['year_of_publication'] >= year_range[0]) & (filtered_data['year_of_publication'] <= year_range[1])]
        if rating_range is not None:
            filtered_data = filtered_data[(filtered_data['rating'] >= rating_range[0]) & (filtered_data['rating'] <= rating_range[1])]
        return filtered_data

col1, col2 = st.columns(2)

with col1:
        with st.expander("Parameters:"):
            # Create widgets
            axes_options = ['age', 'year_of_publication', 'rating']
            x_axis = st.selectbox('Select X axis', axes_options)
            y_axis = st.selectbox('Select Y axis', axes_options)

            age_range = None
            year_range = None
            rating_range = None

            if 'age' in [x_axis, y_axis]:
                age_range = st.slider('Age Range', 5, 99, (5, 99))
            if 'year_of_publication' in [x_axis, y_axis]:
                year_range = st.slider('Year of Publication Range', 1800, 2024, (1800, 2024))
            if 'rating' in [x_axis, y_axis]:
                rating_range = st.slider('Rating', 0, 10, (0, 10))

with col2:
            if st.button('Plot'):
                filtered_data = filter_data(maindata, x_axis, y_axis, age_range, year_range, rating_range)
                fig = px.scatter(filtered_data, x=x_axis, y=y_axis, size='rating', color='rating', hover_name='book_title', title='Bubble Plot of Book Ratings')
                st.plotly_chart(fig)

st.markdown('[Return to Dashboard](http://localhost:8511)', unsafe_allow_html=True)