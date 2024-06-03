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

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

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
    agglomerative_model = joblib.load('salad_clustering_machine.pkl')
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

df = pd.read_csv('C:/Users/msais/Desktop/gitrepos/Saladicious-LangChain/salads_to_date.csv')
df.columns = ['text','orders']
df['processed_text'] = df['text'].apply(lambda x: preprocess_text(x))
df['category'] = df['processed_text'].apply(lambda x: assign_to_cluster(x))


print(df)
average_orders = df.groupby('category')['orders'].mean()
print(average_orders)
print(df['category'].value_counts())
df.to_csv('salads_clustered.csv', index=False)
