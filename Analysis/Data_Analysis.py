import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template
import random
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# def analyze_data(scraped_data):
#     # Analyze the data (sales and rating distributions)
#     print('This is scarpped data in analyze data', scraped_data)
#     prices = [gig['price'] for gig in scraped_data]
#     ratings = [gig['Rating'] for gig in scraped_data]
#     rating_counts = [gig['RatingCount'] for gig in scraped_data]
  
#     # Sales distribution
#     low_sales = sum(1 for price in prices if price < 40)
#     medium_sales = sum(1 for price in prices if 40 <= price < 60)
#     high_sales = sum(1 for price in prices if price >= 60)
  
#     sales_distribution = {'low_sales': low_sales, 'medium_sales': medium_sales, 'high_sales': high_sales}
  
#     # Rating distribution
#     low_rating = sum(1 for rating in ratings if rating < 4.0)
#     medium_rating = sum(1 for rating in ratings if 4.0 <= rating < 4.5)
#     high_rating = sum(1 for rating in ratings if rating >= 4.5)
  
#     rating_distribution = {'low_rating': low_rating, 'medium_rating': medium_rating, 'high_rating': high_rating}
  
#     # Average rating
#     # avg_rating = sum(ratings) / len(ratings)
  
#     # Return all analysis results
#     return {
#         'sales_distribution': sales_distribution,
#         'rating_distribution': rating_distribution,
#         # 'avg_rating': avg_rating
#     }

def analyze_data(scrapped_data):
    """
    Analyze the scraped data, extracting focus and unique keywords from the title 
    and identifying low and high sales based on price.
    :param scrapped_data: List of dictionaries containing scraped data.
    :return: Dictionary with keyword analysis and sales analysis.
    """
    # Extract titles
    titles = [item['title'] for item in scrapped_data if 'title' in item]
  
    # Combine all titles into a single text
    all_titles_text = " ".join(titles).lower()
  
    # Tokenize the text (removing special characters and splitting by whitespace)
    tokens = re.findall(r'\b\w+\b', all_titles_text)
  
    # Count the frequency of each keyword
    keyword_counts = Counter(tokens)
  
    # Focus keywords: Words with the highest frequency
    focus_keywords = keyword_counts.most_common(10)  # Top 10 keywords
  
    # Unique keywords: Words that appear only once
    unique_keywords = [word for word, count in keyword_counts.items() if count == 1]    # Extract prices and preprocess them
    prices = []
    for item in scrapped_data:
        price = item.get('price', '')  # Get price, default to empty string
        if price:
            # Extract numeric part of price (remove 'PKR', commas, etc.)
            numeric_price = re.sub(r'[^\d]', '', price)
            if numeric_price.isdigit():  # Ensure it's a valid number
                prices.append(int(numeric_price))
  
    # Sales analysis
    low_sales = sum(1 for price in prices if price < 40000)  # Example threshold: 40,000 PKR
    high_sales = sum(1 for price in prices if price >= 40000)    
    return {
        "focus_keywords": focus_keywords,
        "unique_keywords": unique_keywords,
        "low_sales_count": low_sales,
        "high_sales_count": high_sales,
        "price_count": len(prices)  # Total valid prices processed
    }

# Step 3: Define the Plotly Visualizations
# 


def generate_wordcloud(unique_keywords):
    """
    Generate a word cloud from the unique keywords.
    :param unique_keywords: List of unique keywords.
    :return: HTML string of the word cloud image.
    """
    # Join the unique keywords into a single string
    text = " ".join(unique_keywords)

    # Create a WordCloud object
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white',
        colormap='viridis'
    ).generate(text)

    # Save the word cloud image to a buffer
    buffer = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Convert the image to base64 for embedding in HTML
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    # Return the HTML image tag with the base64-encoded image
    return f'<img src="data:image/png;base64,{img_str}" alt="Word Cloud">'

def plot_focus_keywords(focus_keywords):
    keywords = [keyword for keyword, count in focus_keywords]
    counts = [count for keyword, count in focus_keywords]
    
    fig = go.Figure(data=[go.Bar(x=keywords, y=counts, marker_color='lightblue')])
    fig.update_layout(
        title='Top Focus Keywords',
        xaxis_title='Keywords',
        yaxis_title='Frequency',
        xaxis_tickangle=-45
    )
    return fig.to_html(full_html=False)

# Visualize Sales Distribution
def plot_sales_distribution(low_sales, high_sales):
    categories = ['Low Sales', 'High Sales']
    counts = [low_sales, high_sales]
    
    fig = go.Figure(data=[go.Bar(x=categories, y=counts, marker_color=['red', 'green'])])
    fig.update_layout(
        title='Sales Distribution',
        xaxis_title='Sales Categories',
        yaxis_title='Number of Gigs'
    )
    return fig.to_html(full_html=False)

# Visualize Unique Keywords Count
def plot_unique_keywords_count(unique_keywords):
    unique_count = len(unique_keywords)
    
    fig = go.Figure(data=[go.Bar(x=['Unique Keywords'], y=[unique_count], marker_color='orange')])
    fig.update_layout(
        title='Count of Unique Keywords',
        yaxis_title='Count',
        xaxis=dict(tickvals=['Unique Keywords'])
    )
    return fig.to_html(full_html=False)