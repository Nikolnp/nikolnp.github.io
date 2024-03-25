import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

@st.cache
def load_data():
    df_strings = pd.read_excel('molecules_task.xlsx', sheet_name='Strings')
    df_targets = pd.read_excel('molecules_task.xlsx', sheet_name='Targets')
    return df_strings, df_targets

def compute_similarity(df_strings, df_targets):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_strings = tfidf_vectorizer.fit_transform(df_strings['String'])
    tfidf_targets = tfidf_vectorizer.transform(df_targets['Target'])
    cosine_similarities = cosine_similarity(tfidf_strings, tfidf_targets)
    most_similar_indices = cosine_similarities.argmax(axis=1)
    most_similar_scores = cosine_similarities.max(axis=1)
    mapped_targets = [df_targets.loc[idx, 'Target'] for idx in most_similar_indices]
    df_strings['mapped_target'] = mapped_targets
    df_strings['similarity_score'] = most_similar_scores
    return df_strings

def main():
    st.title("Molecules Analysis")

    # Load data
    df_strings, df_targets = load_data()

    # Compute similarity
    df_strings = compute_similarity(df_strings, df_targets)

    # Display the mapped targets and similarity scores
    st.subheader("Mapped Targets and Similarity Scores")
    st.write(df_strings[['String', 'mapped_target', 'similarity_score']])

    # Visualize some insights
    st.subheader("Visualizations")

    # Histogram of similarity scores
    st.pyplot(plot_histogram(df_strings['similarity_score']))

    # Word Cloud of Strings
    st.pyplot(plot_word_cloud(df_strings['String']))

    # Scatter Plot of Similarity Scores
    st.pyplot(plot_scatter_similarity(df_strings['similarity_score']))

    # Bar Plot of Target Lengths
    st.pyplot(plot_bar_target_lengths(df_targets))

    # Top 10 Most Common Mapped Targets
    st.subheader("Top 10 Most Common Mapped Targets")
    st.write(df_strings['mapped_target'].value_counts().head(10))

    # Pie Chart of Top 10 Most Common Mapped Targets
    st.pyplot(plot_pie_chart(df_strings))

    # Cluster Analysis
    st.subheader("Cluster Analysis")
    st.pyplot(plot_cluster_analysis(df_strings))

def plot_histogram(similarity_scores):
    plt.figure(figsize=(10, 6))
    plt.hist(similarity_scores, bins=20, color='skyblue')
    plt.xlabel('Similarity Score', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Similarity Scores', fontsize=16)
    return plt

def plot_word_cloud(strings):
    plt.figure(figsize=(10, 6))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(strings))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word Cloud of Strings', fontsize=16)
    plt.axis('off')
    return plt

def plot_scatter_similarity(similarity_scores):
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(similarity_scores)), similarity_scores, alpha=0.5, color='orange')
    plt.title('Scatter Plot of Similarity Scores', fontsize=16)
    plt.xlabel('String Index', fontsize=12)
    plt.ylabel('Similarity Score', fontsize=12)
    return plt

def plot_bar_target_lengths(df_targets):
    plt.figure(figsize=(10, 6))
    df_targets['target_length'] = df_targets['Target'].apply(lambda x: len(x.split()))
    df_targets['target_length'].value_counts().sort_index().plot(kind='bar', color='lightgreen')
    plt.title('Distribution of Target Molecule Lengths', fontsize=16)
    plt.xlabel('Number of Words', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    return plt

def plot_pie_chart(df_strings):
    plt.figure(figsize=(8, 8))
    top_10_mapped_targets = df_strings['mapped_target'].value_counts().head(10)
    plt.pie(top_10_mapped_targets, labels=top_10_mapped_targets.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab10.colors)
    plt.title('Top 10 Most Common Mapped Targets', fontsize=16)
    plt.axis('equal')
    return plt

def plot_cluster_analysis(df_strings):
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(df_strings['similarity_score'].values.reshape(-1, 1))
    plt.figure(figsize=(10, 6))
    plt.scatter(df_strings['similarity_score'], df_strings['mapped_target'].map(df_strings['mapped_target'].value_counts()), c=clusters, cmap='viridis', alpha=0.5)
    plt.title('Cluster Analysis of Similarity Scores and Target Frequency', fontsize=16)
    plt.xlabel('Similarity Score', fontsize=12)
    plt.ylabel('Target Frequency', fontsize=12)
    plt.colorbar(label='Cluster')
    return plt

if __name__ == "__main__":
    main()
