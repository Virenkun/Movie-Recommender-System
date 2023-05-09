import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d784d04122e459c212ceba977419d53c&language=en-US'.format(movie_id))
    data = response.json()
    if 'poster_path' in data:
        str1 = "https://image.tmdb.org/t/p/w500"
        str2 = data['poster_path']
        return str1 + str2
    else:
        return None


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')


def recommend(movie):
    # index fetching
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(similarity[0])), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from api
        poster_url = fetch_poster(movie_id)
        if poster_url is not None:
            recommend_movies_poster.append(poster_url)
            recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies, recommend_movies_poster


selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)


if st.button('Recommend'):
    st.title(selected_movie_name)
    name, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])