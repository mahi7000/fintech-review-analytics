# scripts/generate_plots.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def build_analytics_dashboard():
    csv_path = "data/processed_analytics.csv"
    if not os.path.exists(csv_path):
        print("Error: Processed data file missing.")
        return

    df = pd.read_csv(csv_path)
    sns.set_theme(style="whitegrid")
    os.makedirs("data", exist_ok=True)

    # Plot 1: Sentiment Distribution by Bank
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='bank', hue='sentiment_label', palette={'POSITIVE': '#2ec4b6', 'NEGATIVE': '#e71d36', 'NEUTRAL': '#ff9f1c'})
    plt.title('Sentiment Distribution Across Ethiopian Banking Apps', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Bank Name', fontweight='bold')
    plt.ylabel('Review Count', fontweight='bold')
    plt.legend(title='Sentiment')
    plt.tight_layout()
    plt.savefig('data/plot_sentiment_by_bank.png', dpi=300)
    plt.close()

    # Plot 2: Rating Distribution Boxplot (Averages and Spread)
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x='bank', y='rating', palette='Set2')
    plt.title('User Rating Spread and App Scores', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Bank Name', fontweight='bold')
    plt.ylabel('Star Rating (1-5)', fontweight='bold')
    plt.tight_layout()
    plt.savefig('data/plot_ratings_distribution.png', dpi=300)
    plt.close()

    # Plot 3: Theme Frequency Matrix across Banks
    plt.figure(figsize=(12, 6))
    theme_data = df.groupby(['bank', 'identified_theme']).size().reset_index(name='count')
    sns.barplot(data=theme_data, y='identified_theme', x='count', hue='bank', palette='muted')
    plt.title('Operational Issues and Feature Mention Counts by Bank', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Number of Mentions', fontweight='bold')
    plt.ylabel('Extracted Product Theme', fontweight='bold')
    plt.tight_layout()
    plt.savefig('data/plot_theme_frequency.png', dpi=300)
    plt.close()

    print("All business intelligence plots exported successfully into the data/ folder.")

if __name__ == "__main__":
    build_analytics_dashboard()