import pandas as pd
#import matplotlib.pyplot as plt
#from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

# Load the Excel file into pandas dataframe
df_strings = pd.read_excel('molecules_task.xlsx', sheet_name='Strings')
df_targets = pd.read_excel('molecules_task.xlsx', sheet_name='Targets')

# Create TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the strings
tfidf_strings = tfidf_vectorizer.fit_transform(df_strings['String'])

# Transform targets
tfidf_targets = tfidf_vectorizer.transform(df_targets['Target'])

# Compute cosine similarity between strings and targets
cosine_similarities = cosine_similarity(tfidf_strings, tfidf_targets)

# Find the most similar target for each string
most_similar_indices = cosine_similarities.argmax(axis=1)
most_similar_scores = cosine_similarities.max(axis=1)

# Map strings to targets
mapped_targets = [df_targets.loc[idx, 'Target'] for idx in most_similar_indices]

# Add mapped targets to the strings dataframe
df_strings['mapped_target'] = mapped_targets
df_strings['similarity_score'] = most_similar_scores

# Output the mapped targets and similarity scores
print(df_strings[['String', 'mapped_target', 'similarity_score']])

# Visualize some insights

# 1. Plot histogram of similarity scores
plt.figure(figsize=(10, 6))
plt.hist(df_strings['similarity_score'], bins=20, color='skyblue')
plt.xlabel('Similarity Score', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Similarity Scores', fontsize=16)
plt.show()

# 2. Word Cloud of Strings
plt.figure(figsize=(10, 6))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df_strings['String']))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Strings', fontsize=16)
plt.axis('off')
plt.show()

# 3. Relationship between Similarity Score and Target Frequency
plt.figure(figsize=(10, 6))
target_counts = df_strings['mapped_target'].value_counts()
plt.scatter(df_strings['similarity_score'], df_strings['mapped_target'].map(target_counts), color='salmon')
plt.title('Relationship between Similarity Score and Target Frequency', fontsize=16)
plt.xlabel('Similarity Score', fontsize=12)
plt.ylabel('Target Frequency', fontsize=12)
plt.show()

# 4. Bar Plot of Target Lengths
plt.figure(figsize=(10, 6))
df_targets['target_length'] = df_targets['Target'].apply(lambda x: len(x.split()))
df_targets['target_length'].value_counts().sort_index().plot(kind='bar', color='lightgreen')
plt.title('Distribution of Target Molecule Lengths', fontsize=16)
plt.xlabel('Number of Words', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.show()

# 5. Scatter Plot of Similarity Scores
plt.figure(figsize=(10, 6))
plt.scatter(range(len(df_strings)), df_strings['similarity_score'], alpha=0.5, color='orange')
plt.title('Scatter Plot of Similarity Scores', fontsize=16)
plt.xlabel('String Index', fontsize=12)
plt.ylabel('Similarity Score', fontsize=12)
plt.show()

# 6. Displaying the top 10 most common mapped targets in a table
top_10_mapped_targets = df_strings['mapped_target'].value_counts().head(10)
print("\nTop 10 Most Common Mapped Targets:")
print(top_10_mapped_targets.to_frame().reset_index().rename(columns={'index': 'Mapped Target', 'mapped_target': 'Frequency'}))

# 7. Plotting the pie chart for top 10 most common mapped targets
plt.figure(figsize=(8, 8))
plt.pie(top_10_mapped_targets, labels=top_10_mapped_targets.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab10.colors)
plt.title('Top 10 Most Common Mapped Targets', fontsize=16)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn



# Plotting the donut chart for top 10 most common mapped targets
plt.figure(figsize=(8, 8))
colors = plt.cm.tab10.colors
plt.pie(top_10_mapped_targets, labels=top_10_mapped_targets.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Top 10 Most Common Mapped Targets', fontsize=16)
# Draw a circle at the center to make it a donut chart
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.show()

# 8. Cluster Analysis
# Perform K-means clustering with explicit n_init value
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
clusters = kmeans.fit_predict(tfidf_strings)

# Add cluster labels to the dataframe
df_strings['cluster'] = clusters

# Visualize the clusters using a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df_strings['similarity_score'], df_strings['mapped_target'].map(target_counts), c=clusters, cmap='viridis', alpha=0.5)
plt.title('Cluster Analysis of Similarity Scores and Target Frequency', fontsize=16)
plt.xlabel('Similarity Score', fontsize=12)
plt.ylabel('Target Frequency', fontsize=12)
plt.colorbar(label='Cluster')
plt.show()
