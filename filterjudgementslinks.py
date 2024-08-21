import pandas as pd
from db import db

# Step 1: Read CSV file into a DataFrame
csv_file_path = 'data\judgement_links.csv'
df = pd.read_csv(csv_file_path)

# Step 2: Connect to MongoDB and retrieve docUrls
                  # Replace with your database name
collection = db['consumer_case_judgements']             # Replace with your collection name

# Retrieve the list of docUrls from MongoDB
mongo_doc_urls = collection.distinct('document_link')

print('mongo_doc_urls')
# Step 3: Filter out records from CSV that are present in MongoDB
filtered_df = df[~df['link'].isin(mongo_doc_urls)]

# Step 4: (Optional) Save the filtered list back to a new CSV file
filtered_csv_file_path = 'filtered_file.csv'
filtered_df.to_csv(filtered_csv_file_path, index=False)

print(f"Filtered records saved to {filtered_csv_file_path}")
