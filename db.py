from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()



def get_database()-> MongoClient:
   CONNECTION_STRING =   os.environ.get('MONGO_CONNECTION_STRING')
   print("Connection",CONNECTION_STRING)
   client = MongoClient(CONNECTION_STRING)


   print("Connected to mongodb")
   return client['research_engine']
  

db = get_database()

def insert_data(data):
    db.consumer_case_judgements.insert_one(data)
    print("Inserted",data.get('title'))