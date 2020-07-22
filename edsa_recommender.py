"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# import label encoder
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')
movies = pd.read_csv('resources/data/movies.csv')
imdb = pd.read_csv('resources/data/imdb_data.csv')
tags = pd.read_csv('resources/data/tags.csv')
train = pd.read_csv('resources/data/train.csv')
# test = pd.read_csv('resources/data/test.csv')
g_tags = pd.read_csv('resources/data/genome_tags.csv')
g_scores = pd.read_csv('resources/data/genome_scores.csv')
# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Exploratory Data Analysis", "Solution Overview"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    
    if page_selection == "Exploratory Data Analysis":
        st.title("Exploratory Data Analysis")
        ########## Movie count plot ###########
        # Ensure movies['genres'] column contains strings and split into a list of genres
        movies['genres'] = movies['genres'].apply(str).apply(lambda x: x.split('|'))

        # Create a label binarizer class
        mlb = MultiLabelBinarizer()

        # Create a new dataframe with the binarized genres
        df_genres = pd.DataFrame(mlb.fit_transform(movies['genres']), columns=mlb.classes_)
        df = pd.merge(left=movies,right=df_genres, left_index=True, right_index=True)
        #df = pd.merge(left=movies,right=df_genres, left_index=True, right_index=True)
        a = pd.melt(df_genres)
        plt.figure(figsize=(10,8))
        sns.countplot(data=a.loc[a['value'] == 1], y='variable', palette = 'viridis')
        plt.title('* Some movies are labelled with multiple genres')
        plt.suptitle('Number of movies belonging to each category', fontsize=15)
        plt.xlabel('Count')
        plt.ylabel('')
        st.pyplot()

        # ###### pie chart plot  #########
        # Calculate the number of ratings per genre of movie
        df_genres['movieId'] = df['movieId']
        genre_ratings = pd.merge(left=train, right=df_genres, left_on='movieId', right_on='movieId')
        genre_ratings.drop(['userId', 'movieId', 'timestamp'], axis=1, inplace=True)
        genre_ratings = genre_ratings.groupby(by=['rating'], axis=0).sum()

        # Examine how the different movie genres are historically rated by users
        names = list(genre_ratings.columns)
        labels = list(genre_ratings.index)
        colours = sns.color_palette(palette='viridis', n_colors=len(labels), desat=None)

        fig = plt.figure()
        fig.subplots_adjust(hspace=1, wspace=1)
        for i in range(1, 21):
            plt.subplot(4, 5, i)
            plt.pie(genre_ratings[names[i-1]], colors=colours, radius=1.8, autopct='%0.1f%%',pctdistance=1.2)
            fig.set_size_inches(20, 16)
            plt.title(names[i-1], pad=58, fontsize=14)
        plt.legend(labels, title='Rating', fancybox=True, loc=6, bbox_to_anchor=(1.8, 6.5))
        st.pyplot()

        # Examine movie ratings from all users
        plt.figure(figsize=(6,4))
        sns.countplot(train['rating'], palette = 'viridis')
        plt.title('Distribution of ratings from all users')
        plt.xlabel('Rating')
        plt.ylabel('Count')
        st.pyplot()
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
