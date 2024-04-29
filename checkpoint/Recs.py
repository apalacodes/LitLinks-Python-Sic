import streamlit as st
import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ratings = pd.read_csv(r"C:\Users\apala\OneDrive\Documents\PythonScripts\project\Untitled Folder\jup\BX-Book-Ratings.csv", encoding='utf-8', encoding_errors='surrogateescape', on_bad_lines='skip', sep=';')
df = pd.read_csv(r"C:\Users\apala\OneDrive\Documents\PythonScripts\project\Untitled Folder\streamlitstuff\Data_Pre.csv", compression='gzip')
unique_books = df.drop_duplicates(subset=['book_title'])
search_table = unique_books[["isbn", "rating", "book_title", "book_author","clean title"]]
search_table.reset_index(drop=True, inplace=True)


vect = TfidfVectorizer(ngram_range=(1,2))
tfidf = vect.fit_transform(search_table["clean title"])

def search(title):
    query_vec = vect.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -12)[-12:]
    return search_table.iloc[indices][::-1]

def find_similar(book_id):
    similar_users = ratings[(ratings["ISBN"] == book_id) & (ratings['Book-Rating'] >= 5)]["User-ID"].unique()
    similar_user_recs = ratings[(ratings["User-ID"].isin(similar_users)) & (ratings['Book-Rating'] >= 4) & (ratings["ISBN"] != book_id)]
    if similar_user_recs.empty:
        return "Sorry, we don't have recommendations for you :( \n Check out the Popular Picks !"
    else:
        average_ratings = similar_user_recs.groupby("ISBN")["Book-Rating"].mean()
        highly_rated_books = average_ratings.sort_values(ascending=False)
        return highly_rated_books

st.title("Book Recommendation System")

book_input = st.text_input("Enter Book Title:", "")
book_list = st.empty()

if book_input:
    results = search(book_input)
    if not results.empty:
        book_id = results.iloc[0]["isbn"]
        recommendations = find_similar(book_id)
        if isinstance(recommendations, str):
            st.write(recommendations)
        else:
            recommended_titles = search_table[search_table["isbn"].isin(recommendations.index)]["book_title"].head(12)
            num_columns = 3
            num_rows = len(recommended_titles) // num_columns + (len(recommended_titles) % num_columns > 0)
            columns = st.columns(num_columns)
            for i in range(num_rows):
                for j in range(num_columns):
                    index = i * num_columns + j
                    if index < len(recommended_titles):
                        with columns[j]:
                            box = st.container(border=True, height=100)
                            with box:
                                st.write(recommended_titles.iloc[index])  
    else:
        st.write("Sorry, we don't have recommendations for you :( \n Check out the Popular Picks !")

st.markdown('[Return to Dashboard](http://192.168.1.13:8509)', unsafe_allow_html=True)
