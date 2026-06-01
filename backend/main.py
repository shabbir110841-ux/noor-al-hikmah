from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import json
import os

app = FastAPI()

# CORS Middleware (allows your frontend website to read this API safely)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your MongoDB Atlas Connection String
MONGO_URI = "mongodb+srv://shabbir110841_db_user:vXS46JIsN4buehGX@cluster0.bv2fwxa.mongodb.net/?appName=Cluster0"

# Connect to the MongoDB Cloud
client = MongoClient(MONGO_URI)
db = client["NoorAlHikmah"]
books_collection = db["books"]

@app.on_event("startup")
def startup_db_client():
    # If the database collection is empty, automatically seed it with your JSON data
    if books_collection.count_documents({}) == 0:
        print("MongoDB is empty! Seeding data from dummy_data.json...")
        try:
            json_path = os.path.join(os.path.dirname(__file__), "dummy_data.json")
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                # Insert the books list into MongoDB
                books_collection.insert_many(data["books"])
            print("Database successfully seeded with your Hadith books!")
        except Exception as e:
            print(f"Error seeding database: {e}")
    else:
        print("Database already contains books. Ready to go!")

@app.get("/")
def home():
    return {"message": "Welcome to the Noor Al Hikmah API! Connected successfully to MongoDB Cloud."}

@app.get("/api/books")
def get_books():
    # Fetch all books from MongoDB, hiding the internal '_id' field MongoDB adds automatically
    books = list(books_collection.find({}, {"_id": 0}))
    return {"books": books}