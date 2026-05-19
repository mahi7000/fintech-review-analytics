import os
import pandas as pd
from sqlalchemy import create_engine, text

DB_USER = "postgres"
DB_PASS = "postgresql"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bank_reviews"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def load_data_to_postgres():
    csv_path = "data/processed_analytics.csv"
    if not os.path.exists(csv_path):
        print(f"Error: Enriched analytics file not found at {csv_path}. Run preprocessing first.")
        return
    
    df = pd.read_csv(csv_path)

    rename_map = {}
    if 'review' in df.columns:
        rename_map['review'] = 'review_text'
    if 'date' in df.columns:
        rename_map['date'] = 'review_date'
        
    if rename_map:
        print(f"🔄 Standardizing column headers: {rename_map}")
        df = df.rename(columns=rename_map)

    engine = create_engine(DATABASE_URL)

    print("Connecting to PostgreSQL and creating schema...")
    with engine.connect() as conn:
        with open("scripts/schema.sql", "r") as f:
            schema_sql = f.read()
        conn.execute(text(schema_sql))
        conn.commit()
    print("Database schema initialized successfully.")

    # Populate Banks Table Metadata
    banks_df = pd.DataFrame([
        {"bank_name": "CBE", "app_name": "Commercial Bank of Ethiopia Mobile"},
        {"bank_name": "BOA", "app_name": "Bank of Abyssinia Mobile"},
        {"bank_name": "Dashen", "app_name": "Dashen Bank Mobile"}
    ])
    
    print("Inserting bank metadata records...")
    banks_df.to_sql("banks", engine, if_exists="append", index=False)

    with engine.connect() as conn:
        db_banks = pd.read_sql(text("SELECT bank_id, bank_name FROM banks"), conn)
    
    bank_id_map = dict(zip(db_banks['bank_name'], db_banks['bank_id']))
    df['bank_id'] = df['bank'].map(bank_id_map)

    final_reviews_table = df[[
        'review_id', 'bank_id', 'review_text', 'rating', 
        'review_date', 'sentiment_label', 'sentiment_score', 'identified_theme', 'source'
    ]]

    print(f"Loading {len(final_reviews_table)} structured reviews into PostgreSQL...")
    final_reviews_table.to_sql("reviews", engine, if_exists="append", index=False)
    
    # Run verification queries to prove data integrity
    print("\n================ Data Integrity Verification ================")
    with engine.connect() as conn:
        total_reviews = conn.execute(text("SELECT COUNT(*) FROM reviews")).scalar()
        print(f"Total reviews stored in database: {total_reviews}")
        
        print("\nAverage rating and review count per bank app:")
        metrics = pd.read_sql(text("""
            SELECT b.bank_name, COUNT(r.review_id) as total_reviews, ROUND(AVG(r.rating), 2) as avg_rating
            FROM reviews r
            JOIN banks b ON r.bank_id = b.bank_id
            GROUP BY b.bank_name;
        """), conn)
        print(metrics.to_string(index=False))
    print("============================================================\n")

if __name__ == "__main__":
    load_data_to_postgres()