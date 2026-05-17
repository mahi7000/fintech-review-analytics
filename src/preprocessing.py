import pandas as pd
import os

def clean_data(input_path="data/raw/raw_reviews.csv", output_path="data/cleaned_reviews.csv"):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Raw data file {input_path} not found.")
    
    df = pd.read_csv(input_path)

    df = df.dropna(subset=['review', 'rating'])
    df = df.drop_duplicates(subset=['review', 'rating', 'bank'])

    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df = df[['review', 'rating', 'date', 'bank', 'source']]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Preprocessing complete. Clean records: {len(df)}")
    return df

if __name__ == "__main__":
    clean_data()