import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load the dataset
movies = pd.read_csv('imdb_top_1000.csv')

# Handle missing values
movies.fillna('', inplace=True)


movies['Genre'] = movies['Genre'].str.lower()
movies['Certificate'] = movies['Certificate'].str.lower()

# Create a TF-IDF Vectorizer for the 'Genre' and 'Certificate' or Convert text into integer form and create matrix.
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(movies['Genre'] + ' ' + movies['Certificate'])

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(genre, certificate, imdb_rating):
    # Filter movies based on user input
    filtered_movies = movies[(movies['Genre'].str.contains(genre)) & 
                             (movies['Certificate'].str.contains(certificate)) & 
                             (movies['IMDB_Rating'] >= imdb_rating)]
    
    if filtered_movies.empty:
        return "No movies found for the specified criteria." 
    
    # Get indices of the filtered movies
    indices = filtered_movies.index.tolist()
    
    # Calculate similarity scores for the filtered movies
    sim_scores = list(enumerate(cosine_sim[indices]))
    
    # Sort the movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1].sum(), reverse=True)
    
    # Store top 6 movies
    top_movies_indices = [i[0] for i in sim_scores[:6]]
    
    # Create a list of recommended movies
    recommended_movies = filtered_movies.iloc[top_movies_indices][['Poster_Link', 'Series_Title', 'Genre', 'Certificate', 'IMDB_Rating', 'Overview', 'Runtime', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']].to_dict(orient='records')

    return recommended_movies  # Return the lists