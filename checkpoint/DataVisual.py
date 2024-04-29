import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import cm
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline
from wordcloud import WordCloud, STOPWORDS
from sklearn.preprocessing import MinMaxScaler
from cleancountry import visualize_book_distribution
st.set_page_config(page_title="Data Visualization & Reccomendation", layout='wide',initial_sidebar_state='expanded')
sidebar_options = ["🏠 Home","Data Preview 👀","📊Data Visualization","Customizable Bubble Plot 🫧","🌟Popular Picks","Personalized Recommendations 🔍"]
st.sidebar.title("Navigation Bar")

def home():
    st.title("Welcome to **LitLinks**📚")
    box=st.container(border=True)
    with box:
        st.markdown("### Torn between which book to choose next after absolutely devouring a 🌟🌟🌟🌟🌟-star masterpiece? We've got you covered with personalized recommendations tailored just for you with **LitLinks**!! \n With an array of data visuals and customizable plots, allowing you to effortlessly navigate through a sea of literary wonders. Discover popular picks that resonate with readers worldwide, uncover insights into top authors and publications, and venture into the essence of storytelling like never before.")
def data():
    st.header(" Data Preview 👀")
    @st.cache_data
    def load_data(file_path):
                data = pd.read_csv(file_path, compression='gzip')
                return data
    maindata = load_data(r"C:\Users\apala\OneDrive\Documents\PythonScripts\project\Untitled Folder\streamlitstuff\Data_Pre.csv")
            
    st.markdown("### Total Counts")
    col1, col2, col3, col4 = st.columns(4)
    bookc = maindata["book_title"].nunique()
    authorc = maindata["book_author"].nunique()
    userc = maindata["user_id"].nunique()
    ratingc = maindata["rating"].count()
    with col1:
                box=st.container(border=True)
                with box:
                    st.markdown("Books")
                    st.subheader(bookc)    
    with col2:
                box=st.container(border=True)
                with box:
                    st.markdown("Authors")
                    st.subheader(authorc) 
    with col3:
                box=st.container(border=True)
                with box:
                    st.markdown("Users")
                    st.subheader(userc) 
    with col4:
                box=st.container(border=True)
                with box:
                    st.markdown("Ratings")
                    st.subheader(ratingc) 
    countrydata = pd.read_csv(r"C:\Users\apala\OneDrive\Documents\PythonScripts\project\Untitled Folder\streamlitstuff\countrydata.csv")
    fig = visualize_book_distribution(countrydata)
    st.plotly_chart(fig)
    with st.expander("Data Preview"):
                df_main = maindata.copy(deep=True)
                df_main.rename(columns = {'user_id':'User ID','age':'Age','isbn':'Book ID','rating':'Rating','book_title':'Book Title','book_author':'Author','year_of_publication':'Publication Year','publisher':'Publisher','country':'Country'}, inplace = True) 
                df_main.drop(columns=['location','state','clean title'], inplace=True)
                st.dataframe(df_main.head(20), column_config={'year_of_publication': st.column_config.NumberColumn(format="%d")})
def visuals():
            st.header("📊Data Visualization")
            @st.cache_data
            def load_data(file_path):
                data = pd.read_csv(file_path, compression='gzip')
                return data
            maindata = load_data(r"C:\Users\apala\OneDrive\Documents\PythonScripts\project\Untitled Folder\streamlitstuff\Data_Pre.csv")
            
            container = st.container(border=True)
            with container:
                col1,col2= st.columns([3,3])

                with col1:
                    container = st.container(border=True)
                    with container:
                            st.write("Book Rating Distribution")
                            ccol1, ccol2,= st.columns(2)
                            
                            with ccol1: 
                                nonullratingdf = maindata[maindata['rating'] != 0]
                                rating_distribution = nonullratingdf['rating'].value_counts().sort_index()
                                fig1 = px.bar(x=rating_distribution.index, y=rating_distribution.values, labels={'x':'Rating', 'y':'Frequency'}, color=rating_distribution.index,
                                            color_continuous_scale='RdBu', title='Distribution of Book Ratings')
                                st.plotly_chart(fig1,use_container_width=True)
                            with ccol2: 
                                    x_values = rating_distribution.index
                                    y_values = rating_distribution.values
                                    x_new = np.linspace(x_values.min(), x_values.max(), 300)
                                    spl = make_interp_spline(x_values, y_values, k=3)
                                    y_smooth = spl(x_new)
                                    fig2 = go.Figure(data=go.Scatter(x=x_new, y=y_smooth, mode='lines+markers'))
                                    fig2.update_layout(title='Spline Curve of Book Ratings Distribution', xaxis_title='Rating', yaxis_title='Smoothed Frequency')
                                    st.plotly_chart(fig2,use_container_width=True)
                    container2 = st.container(border=True)
                    with container2:
                                    nonullaged = maindata.dropna(subset=['age'])
                                    bins = [0, 13, 18, 25, 40, 60, np.inf]
                                    labels = ['Children(0-12)', 'Teens(13-17)', 'Young Adults(18-24)', 'Adults(25-39)', 'Mid-aged Adults(40-59)', 'Senior Adults(60+)']
                                    nonullaged['Age Group'] = pd.cut(nonullaged['age'], bins=bins, labels=labels, right=False)
                                    age_group_counts = nonullaged['Age Group'].value_counts()
                                    sorted_counts = age_group_counts.reindex(labels)
                                    fig = go.Figure(data=[go.Pie(labels=sorted_counts.index, values=sorted_counts.values, 
                                                                textinfo='percent', marker=dict(colors=sorted_counts.index))])

                                    fig.update_layout(title='Distribution of Users by Age Group', showlegend=True)
                                    st.plotly_chart(fig,use_container_width=True,height=500)
                    container5 = st.container(border=True)
                    with container5:
                            nonullratingdf = maindata[maindata['rating'] != 0]
                            nonullratingdf['age_of_book'] = (2024 - nonullratingdf['year_of_publication'])
                            scaler = MinMaxScaler()
                            nonullratingdf[['Age of Book', 'Age Of User', 'Rating']] = scaler.fit_transform(nonullratingdf[['age_of_book', 'age', 'rating']])
                            correlation_matrix = nonullratingdf[['Age of Book', 'Age Of User', 'Rating']].corr(method='pearson')                
                            fig = px.imshow(correlation_matrix, 
                                            labels=dict(x="Variables", y="Variables", color="Correlation"),
                                            x=correlation_matrix.columns,
                                            y=correlation_matrix.columns,
                                            color_continuous_scale='RdPu')
                            fig.update_layout(title="Pearson Correlation Heatmap")
                            st.plotly_chart(fig,use_container_width=True)                   
                            
                with col2:
                    container3 = st.container(border=True)
                    with container3:
                                nonulldf = maindata[maindata['Category'] != '9']
                                category_counts = nonulldf['Category'].value_counts()
                                top_categories = category_counts.head(10)
                                fig = go.Figure(go.Pie(
                                            labels=top_categories.index,
                                            values=top_categories.values,
                                            hole=0.5,
                                            direction='clockwise',
                                            textinfo='percent',
                                            insidetextorientation='radial'
                                        ))
                                fig.update_layout(
                                        title='Top 10 Book Categories',
                                        legend=dict(
                                            x=0.7,
                                            y=0.5,
                                            traceorder='normal',
                                            font=dict(size=10),
                                            title='Categories',
                                            title_font_size=10))
                                st.plotly_chart(fig,use_container_width=True) 

                    with st.expander("Top 25's of All Time"):
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            author_counts = maindata['book_author'].value_counts()
                                            top_authors = author_counts.head(25)
                                            fig = go.Figure(go.Bar(
                                                y=top_authors.index,
                                                x=top_authors.values,
                                                orientation='h',
                                                marker_color='#56cfe1'
                                            ))
                                            fig.update_layout(
                                                title='Top 25 Authors by Number of Books Rated',
                                                xaxis_title='Number of Books Rated',
                                                yaxis_title='Author',
                                                yaxis_autorange='reversed'
                                            )
                                            st.plotly_chart(fig,use_container_width=True)
                                        pass

                                        with col2:
                                            book_reads = maindata['book_title'].value_counts()
                                            top_reads = book_reads.head(25)
                                            fig = go.Figure(go.Bar(
                                                y=top_reads.index,
                                                x=top_reads.values,
                                                orientation='h',
                                                marker_color='turquoise'
                                            ))
                                            fig.update_layout(
                                                title='Top 25 Reads',
                                                xaxis_title='Number of Books Read',
                                                yaxis_title='Book Title',
                                                yaxis_autorange='reversed'
                                            )
                                            st.plotly_chart(fig,use_container_width=True)
                                        pass
                    
                                        with col3:
                                            publication_counts = maindata['publisher'].value_counts()
                                            top_pub = publication_counts.head(25)
                                            fig = go.Figure(go.Bar(
                                                y=top_pub.index,
                                                x=top_pub.values,
                                                orientation='h',
                                                marker_color='lightseagreen'
                                            ))
                                            fig.update_layout(
                                                title='Top 25 Publishers',
                                                xaxis_title='Books Count',
                                                yaxis_title='Publishers',
                                                yaxis_autorange='reversed'
                                            )
                                            st.plotly_chart(fig,use_container_width=True)
                                        pass
                            
                    def color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
                                colormap = cm.get_cmap('rainbow')
                                color_index = random_state.randint(0, 256)
                                color = colormap(color_index)
                                return "rgb({},{},{})".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
                    container4= st.container(border=True)
                    with container4:
                                            st.write("Word Cloud of Book Titles")
                                            wc = WordCloud(background_color="black", max_words=300,
                                                        stopwords=STOPWORDS, max_font_size=256,
                                                        random_state=42, width=700, height=700, color_func=color_func)
                                            wc.generate(' '.join(maindata['book_title']))
                                            fig, ax = plt.subplots(figsize=(8, 8))
                                            plt.imshow(wc, interpolation="bilinear")
                                            plt.axis('off')
                                            st.pyplot(fig,use_container_width=True)  
def popular():
    st.header("Recommendations Based on Popularity Just for You!!!")
    @st.cache_data
    def load_data(file_path):
                            data = pd.read_csv(file_path)
                            return data
    populardata = load_data(r"C:\Users\apala\OneDrive\Documents\PythonScripts\project\Untitled Folder\streamlitstuff\PopTop12.csv")
    num_columns = 3
    num_rows = len(populardata) // num_columns + (len(populardata) % num_columns > 0)
    columns = st.columns(num_columns)
    for i in range(num_rows):
                for j in range(num_columns):
                    index = i * num_columns + j
                    if index < len(populardata):
                        with columns[j]:
                            box = st.container(border=True,height=150)
                            with box:
                                book_name = populardata.iloc[index]["Book Name"]
                                author = populardata.iloc[index]["Authors"]
                                year = populardata.iloc[index]["PublishYear"]
                                rating = populardata.iloc[index]["Rating"]
                                st.markdown(f"**{book_name}**\n*by {author}, {year}, Rating: {rating}*")

item_selected = False  
for item in sidebar_options:
    if st.sidebar.button(item):
        st.empty()
        item_selected = True 
        if item == "🏠 Home":
            home()
        if item == "Data Preview 👀":
            data()
        if item == "📊Data Visualization":
            visuals()
            # st.header("📊Data Visualization")
            # @st.cache_data
            # def load_data(file_path):
            #     data = pd.read_csv(file_path, compression='gzip')
            #     return data
            # maindata = load_data(r"C:\Users\apala\OneDrive\Documents\PythonScripts\project\Untitled Folder\streamlitstuff\Data_Pre.csv")
            
            # container = st.container(border=True)
            # with container:
            #     col1,col2= st.columns([3,3])

            #     with col1:
            #         container = st.container(border=True)
            #         with container:
            #                 st.write("Book Rating Distribution")
            #                 ccol1, ccol2,= st.columns(2)
                            
            #                 with ccol1: 
            #                     nonullratingdf = maindata[maindata['rating'] != 0]
            #                     rating_distribution = nonullratingdf['rating'].value_counts().sort_index()
            #                     fig1 = px.bar(x=rating_distribution.index, y=rating_distribution.values, labels={'x':'Rating', 'y':'Frequency'}, color=rating_distribution.index,
            #                                 color_continuous_scale='RdBu', title='Distribution of Book Ratings')
            #                     st.plotly_chart(fig1,use_container_width=True)
            #                 with ccol2: 
            #                         x_values = rating_distribution.index
            #                         y_values = rating_distribution.values
            #                         x_new = np.linspace(x_values.min(), x_values.max(), 300)
            #                         spl = make_interp_spline(x_values, y_values, k=3)
            #                         y_smooth = spl(x_new)
            #                         fig2 = go.Figure(data=go.Scatter(x=x_new, y=y_smooth, mode='lines+markers'))
            #                         fig2.update_layout(title='Spline Curve of Book Ratings Distribution', xaxis_title='Rating', yaxis_title='Smoothed Frequency')
            #                         st.plotly_chart(fig2,use_container_width=True)
            #         container2 = st.container(border=True)
            #         with container2:
            #                         nonullaged = maindata.dropna(subset=['age'])
            #                         bins = [0, 13, 18, 25, 40, 60, np.inf]
            #                         labels = ['Children(0-12)', 'Teens(13-17)', 'Young Adults(18-24)', 'Adults(25-39)', 'Mid-aged Adults(40-59)', 'Senior Adults(60+)']
            #                         nonullaged['Age Group'] = pd.cut(nonullaged['age'], bins=bins, labels=labels, right=False)
            #                         age_group_counts = nonullaged['Age Group'].value_counts()
            #                         sorted_counts = age_group_counts.reindex(labels)
            #                         fig = go.Figure(data=[go.Pie(labels=sorted_counts.index, values=sorted_counts.values, 
            #                                                     textinfo='percent', marker=dict(colors=sorted_counts.index))])

            #                         fig.update_layout(title='Distribution of Users by Age Group', showlegend=True)
            #                         st.plotly_chart(fig,use_container_width=True,height=500)
            #         container5 = st.container(border=True)
            #         with container5:
            #                 nonullratingdf = maindata[maindata['rating'] != 0]
            #                 nonullratingdf['age_of_book'] = (2024 - nonullratingdf['year_of_publication'])
            #                 scaler = MinMaxScaler()
            #                 nonullratingdf[['Age of Book', 'Age Of User', 'Rating']] = scaler.fit_transform(nonullratingdf[['age_of_book', 'age', 'rating']])
            #                 correlation_matrix = nonullratingdf[['Age of Book', 'Age Of User', 'Rating']].corr(method='pearson')                
            #                 fig = px.imshow(correlation_matrix, 
            #                                 labels=dict(x="Variables", y="Variables", color="Correlation"),
            #                                 x=correlation_matrix.columns,
            #                                 y=correlation_matrix.columns,
            #                                 color_continuous_scale='RdPu')
            #                 fig.update_layout(title="Pearson Correlation Heatmap")
            #                 st.plotly_chart(fig,use_container_width=True)                   
                            
            #     with col2:
            #         container3 = st.container(border=True)
            #         with container3:
            #                     nonulldf = maindata[maindata['Category'] != '9']
            #                     category_counts = nonulldf['Category'].value_counts()
            #                     top_categories = category_counts.head(10)
            #                     fig = go.Figure(go.Pie(
            #                                 labels=top_categories.index,
            #                                 values=top_categories.values,
            #                                 hole=0.5,
            #                                 direction='clockwise',
            #                                 textinfo='percent',
            #                                 insidetextorientation='radial'
            #                             ))
            #                     fig.update_layout(
            #                             title='Top 10 Book Categories',
            #                             legend=dict(
            #                                 x=0.7,
            #                                 y=0.5,
            #                                 traceorder='normal',
            #                                 font=dict(size=10),
            #                                 title='Categories',
            #                                 title_font_size=10))
            #                     st.plotly_chart(fig,use_container_width=True) 

            #         with st.expander("Top 25's of All Time"):
            #                             col1, col2, col3 = st.columns(3)
            #                             with col1:
            #                                 author_counts = maindata['book_author'].value_counts()
            #                                 top_authors = author_counts.head(25)
            #                                 fig = go.Figure(go.Bar(
            #                                     y=top_authors.index,
            #                                     x=top_authors.values,
            #                                     orientation='h',
            #                                     marker_color='#56cfe1'
            #                                 ))
            #                                 fig.update_layout(
            #                                     title='Top 25 Authors by Number of Books Rated',
            #                                     xaxis_title='Number of Books Rated',
            #                                     yaxis_title='Author',
            #                                     yaxis_autorange='reversed'
            #                                 )
            #                                 st.plotly_chart(fig,use_container_width=True)
            #                             pass

            #                             with col2:
            #                                 book_reads = maindata['book_title'].value_counts()
            #                                 top_reads = book_reads.head(25)
            #                                 fig = go.Figure(go.Bar(
            #                                     y=top_reads.index,
            #                                     x=top_reads.values,
            #                                     orientation='h',
            #                                     marker_color='turquoise'
            #                                 ))
            #                                 fig.update_layout(
            #                                     title='Top 25 Reads',
            #                                     xaxis_title='Number of Books Read',
            #                                     yaxis_title='Book Title',
            #                                     yaxis_autorange='reversed'
            #                                 )
            #                                 st.plotly_chart(fig,use_container_width=True)
            #                             pass
                    
            #                             with col3:
            #                                 publication_counts = maindata['publisher'].value_counts()
            #                                 top_pub = publication_counts.head(25)
            #                                 fig = go.Figure(go.Bar(
            #                                     y=top_pub.index,
            #                                     x=top_pub.values,
            #                                     orientation='h',
            #                                     marker_color='lightseagreen'
            #                                 ))
            #                                 fig.update_layout(
            #                                     title='Top 25 Publishers',
            #                                     xaxis_title='Books Count',
            #                                     yaxis_title='Publishers',
            #                                     yaxis_autorange='reversed'
            #                                 )
            #                                 st.plotly_chart(fig,use_container_width=True)
            #                             pass
                            
            #         def color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
            #                     colormap = cm.get_cmap('rainbow')
            #                     color_index = random_state.randint(0, 256)
            #                     color = colormap(color_index)
            #                     return "rgb({},{},{})".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
            #         container4= st.container(border=True)
            #         with container4:
            #                                 st.write("Word Cloud of Book Titles")
            #                                 wc = WordCloud(background_color="black", max_words=300,
            #                                             stopwords=STOPWORDS, max_font_size=256,
            #                                             random_state=42, width=700, height=700, color_func=color_func)
            #                                 wc.generate(' '.join(maindata['book_title']))
            #                                 fig, ax = plt.subplots(figsize=(8, 8))
            #                                 plt.imshow(wc, interpolation="bilinear")
            #                                 plt.axis('off')
            #                                 st.pyplot(fig,use_container_width=True)  
        if item == "Customizable Bubble Plot 🫧":
            st.header("Customizable Bubble Plot 🫧")
            st.markdown('[Redirecting...](http://192.168.1.13:8509)', unsafe_allow_html=True)
        if item == "🌟Popular Picks": 
            popular()            
        if item=="Personalized Recommendations 🔍":
            st.header("Personalized Recommendations 🔍")
            st.markdown('[Redirecting...](http://192.168.1.13:8510)', unsafe_allow_html=True)             
        
if item_selected == False:
    st.title("Welcome to **LitLinks**📚")
    box=st.container(border=True)
    with box:
        st.markdown("### Torn between which book to choose next after absolutely devouring a 🌟🌟🌟🌟🌟-star masterpiece? We've got you covered with personalized recommendations tailored just for you with **LitLinks**!! \n With an array of data visuals and customizable plots, allowing you to effortlessly navigate through a sea of literary wonders. Discover popular picks that resonate with readers worldwide, uncover insights into top authors and publications, and venture into the essence of storytelling like never before.")
