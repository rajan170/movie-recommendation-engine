import streamlit as st
import pickle
import pandas as pd
import requests
from config import tmdb_api_key


def movies_overview(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, tmdb_api_key)
    response = requests.get(url)
    data = response.json()
    movie_overview = (data['overview'])
    return movie_overview


def fetch_posters(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, tmdb_api_key)
    response = requests.get(url)
    data = response.json()
    poster_img = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    # movie_overview = (data['overview'])
    return poster_img


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:

        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
        overview = movies_overview(movie_id)
    return recommended_movies, recommended_movies_posters, overview


movies_dict = pickle.load(open("movies_dict.pkl", 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", 'rb'))

st.title("Movie Recommendation Engine")

selected_movie_name = st.selectbox("Enter the Movie Name", movies['title'].values)

if st.button('Recommend'):
    name, posters, overview = recommend(selected_movie_name)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([name[0], name[1], name[2], name[3], name[4]])

    with tab1:
        st.header(name[0])
        st.image(posters[0])
        st.subheader(overview[0:-1])
    with tab2:
        st.header(name[1])
        st.image(posters[1])
        st.subheader(overview[0:-1])
    with tab3:
        st.header(name[2])
        st.image(posters[2])
        st.subheader(overview[0:-1])
    with tab4:
        st.header(name[3])
        st.image(posters[3])
        st.subheader(overview[0:-1])
    with tab5:
        st.header(name[4])
        st.image(posters[4])
        st.subheader(overview[0:-1])

    # for i in range(0, 5):
    #     col_ = "col"+"{}".format(i)
    #     with col_:
    #         st.header(name[i])
    #         st.image(posters[i])
