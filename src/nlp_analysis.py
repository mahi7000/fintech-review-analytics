import os
import pandas as pd
import spacy
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", truncation=True, device=-1)
nlp = spacy.load("en_core_web_sm")

THEME_KEYWORDS = {
    "Transaction Performance": ["slow", "transfer", "pending", "delay", "waiting", "speed", "time", "loading", "transaction"],
    "Account Access Issues": ["login", "password", "otp", "code", "error", "sign in", "lock", "unable", "fail"],
    "UI & Design": ["interface", "beautiful", "clean", "color", "look", "navigation", "ui", "update", "app"],
    "Customer Support": ["help", "support", "call", "agent", "service", "response", "ignore", "bank"]
}

def assign_theme(text):
    text_lower = str(text).lower()
    for theme, keywords in THEME_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return theme
    return "General Feedback"

def generate_task2_plot(df, output_dir="data"):
    print("Generating Task 2 Visualization...")
    sns.set_theme(style="whitegrid")
    
    # Create a clean, grouped horizontal bar chart
    plt.figure(figsize=(11, 6))
    
    theme_order = df['identified_theme'].value_counts().index
    
    sns.countplot(
        data=df, 
        y='identified_theme', 
        hue='sentiment_label', 
        order=theme_order,
        palette={'POSITIVE': "#3cdea5", 'NEGATIVE': "#f87080"}
    )
    
    # Professional plot decorations
    plt.title('Distribution of Customer Sentiments Across Extracted Operational Themes', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Reviews', fontsize=11, fontweight='bold')
    plt.ylabel('Extracted Product Themes', fontsize=11, fontweight='bold')
    plt.legend(title='Sentiment Label', frameon=True, facecolor='white', edgecolor='none')
    
    plt.tight_layout()
    
    # Save chart
    plot_path = os.path.join(output_dir, "task2_theme_sentiment.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Visualization successfully saved to: {plot_path}")

def run_nlp_pipeline(input_path="data/cleaned_reviews.csv", output_path="data/processed_analytics.csv"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Cleaned data file {input_path} not found. Please run preprocessing first.")

    df = pd.read_csv(input_path)
    
    # Apply sentiment analysis
    sentiments = []
    scores = []
    
    print(f"Processing Sentiments for {len(df)} reviews...")
    for text in df['review']:
        try:
            res = sentiment_pipeline(str(text))[0]
            sentiments.append(res['label'])
            scores.append(res['score'])
        except Exception:
            sentiments.append("NEGATIVE") # Safe fallback fallback
            scores.append(0.5)
            
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores
    
    print("Extracting Operational Themes...")
    df['identified_theme'] = df['review'].apply(assign_theme)
    
    df.index.name = 'review_id'
    df = df.reset_index()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("NLP Processing Complete and Saved.")
    
    generate_task2_plot(df)
    
    return df

if __name__ == "__main__":
    run_nlp_pipeline()