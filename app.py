from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)


# TODO: Fetch dataset, initialize vectorizer and LSA here
# Fetch the dataset
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# Apply SVD for dimensionality reduction
svd = TruncatedSVD(n_components=100)  # You can adjust the number of components
X_reduced = svd.fit_transform(X)

def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    # TODO: Implement search engine here
    # return documents, similarities, indices 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    
    # Process the user query
    query_vec = vectorizer.transform([query])
    query_reduced = svd.transform(query_vec)
    
    # Compute cosine similarities
    similarities = cosine_similarity(query_reduced, X_reduced)[0]
    
    # Get the top 5 documents
    top_indices = similarities.argsort()[-5:][::-1]
    top_similarities = similarities[top_indices]
    top_documents = [documents[i] for i in top_indices]
    
    return jsonify({
        'indices': top_indices.tolist(),
        'similarities': top_similarities.tolist(),
        'documents': top_documents
    })

if __name__ == '__main__':
    app.run(debug=True)
