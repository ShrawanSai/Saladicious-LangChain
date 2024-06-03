import regex as re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
import joblib
import random

# Download NLTK data files if not already downloaded
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

df = pd.read_csv('backend/train_salad_clustered.csv')
s_df = pd.read_csv('backend/salads_clustered.csv')

import nltk
from sentence_transformers import SentenceTransformer
from sklearn.cluster import  KMeans
import nltk

# Download NLTK data files
nltk.download('punkt')

# Load the Sentence Transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def removeStopwords(text):
    stop_words = set(stopwords.words('english'))
    # all verbs also must be removed
    words = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(words)
    non_verbs = [word for word, tag in pos_tags if not tag.startswith('VB')]
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words]
    filtered_text = ' '.join(filtered_words)
    return filtered_text

def lemmatization(text):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    lWords = [lemmatizer.lemmatize(word) for word in words]
    lText = ' '.join(lWords)
    return lText

# Preprocess the new text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'oz', '', text)
    text = re.sub(r'lb', '', text)
    text = re.sub(r'[\d_]+', '', text)
    text = removeStopwords(text)
    text = lemmatization(text)
    return text

# Load the trained Agglomerative Clustering model
def load_agglomerative_model():
    agglomerative_model = joblib.load('backend/salad_clustering_machine.pkl')
    return agglomerative_model

# Convert text to embeddings
def text_to_embeddings(text):
    embeddings = model.encode([text])
    return embeddings

# Function to assign new text to the appropriate cluster
def assign_to_cluster(new_text):
    # Load Agglomerative Clustering model
    agglomerative_model = load_agglomerative_model()

    # Preprocess the new text
    preprocessed_text = preprocess_text(new_text)

    # Convert text to embeddings
    new_embeddings = text_to_embeddings(preprocessed_text)

    # Predict cluster for new text
    cluster_label = agglomerative_model.predict(new_embeddings)[0]

    return cluster_label

def suggest_salad_to_user(df,liking,trainig_set = False):

  category_to_suggest = assign_to_cluster(liking)
  print(f'id_{category_to_suggest}')

  if trainig_set:
    category_col = 'cluster_label'
    recipe_col = 'Original_text'

  else:
    category_col = 'category'
    recipe_col = 'text'
  suggestions = df[df[category_col] == category_to_suggest]
  random_suggestions = df.sample(n=3)


  random_suggestions = list(random_suggestions[recipe_col])
  return random_suggestions

def user_also_liked(liking):
   
   try:
      suggestions = suggest_salad_to_user(s_df,liking,False)
      return suggestions
   except:
      suggestions = suggest_salad_to_user(df,liking,True)
      return suggestions
if __name__ == '__main__':
    suggest_for = """

Hawaiian Poke Bowl Salad
Ingredients: - Sushi-grade tuna or salmon - Sushi rice or mixed greens - Avocado - Cucumber - Edamame - Mango - Seaweed salad - Green onions - Sesame seeds - Soy sauce - Sesame oil 
- Rice vinegar - Honey - Ginger - Garlic. Cube sushi-grade tuna or salmon. - Cook sushi rice according to package instructions or wash and dry mixed greens. - 
Dice avocado and cucumber. - Cook edamame. - Dice mango. - Drain seaweed salad. - Slice green onions. - In a large bowl, arrange sushi rice or mixed greens as a 
base and top with cubed fish, avocado, cucumber, edamame, mango, and seaweed salad. - Sprinkle with sliced green onions and sesame seeds. - Prepare dressing by mixing 
soy sauce, sesame oil, rice vinegar, honey, minced ginger, and minced garlic. - Drizzle dressing over salad and toss gently to coat.
"""

    # Suggestions from Training set:
    suggestions = user_also_liked(suggest_for)
    for i in suggestions:
        print(i)
        print("-"*100)

  