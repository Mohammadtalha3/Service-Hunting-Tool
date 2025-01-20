import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import seaborn as sns
from wordcloud import WordCloud

# Load the dataset (assuming it's stored as 'scraped_data.csv')
df = pd.read_csv('D:\Service-Hunting-Tool\Data\machine_learning_projects.csv')

# Keyword Analysis
def keyword_analysis(data, column_name='Title'):
    # Combine all text in the specified column
    text = " ".join(data[column_name].astype(str).tolist())
    words = text.split()
    unique_words = set(words)

    print(f"Total Words: {len(words)}")
    print(f"Unique Words: {len(unique_words)}")

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Word Cloud for Keywords in Listing Titles")
    plt.show()

# Run keyword analysis
keyword_analysis(df)

# Aggregate Statistics
total_sales = df['sales'].sum() if 'sales' in df.columns else "N/A"
average_rating = df['rating'].mean() if 'rating' in df.columns else "N/A"
print(f"Total Sales: {total_sales}")
print(f"Average Rating: {average_rating}")
