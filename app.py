import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"
    except:
        return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id if 'movie_id' in movies.columns else i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie from the list',
    movies['title'].values)

if st.button('Recommend movies'):
    try:
        names, posters = recommend(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")