import os
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["snapshot"]
users_collection = db["users"]
posts_collection = db["posts"]
gallery_collection = db["gallery"]

def upload_gallery_images(gallery_path='data/gallery'):
    if not os.path.exists(gallery_path):
        print(f"Gallery path '{gallery_path}' does not exist.")
        return

    for filename in os.listdir(gallery_path):
        filepath = os.path.join(gallery_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                image_data = f.read()
                gallery_collection.insert_one({
                    'filename': filename,
                    'data': image_data,
                    'content_type': 'image/jpeg'  # or detect type
                })
    print("Gallery images uploaded successfully.")

def upload_posts(posts_file='data/posts.json'):
    if not os.path.exists(posts_file):
        print(f"Posts file '{posts_file}' does not exist.")
        return

    with open(posts_file, 'r') as f:
        posts = json.load(f)
        if posts:
            posts_collection.insert_many(posts)
    print("Posts uploaded successfully.")

def upload_users(users_file='users.json'):
    if not os.path.exists(users_file):
        print(f"Users file '{users_file}' does not exist.")
        return

    with open(users_file, 'r') as f:
        users = json.load(f)
        if users:
            users_collection.insert_many(users)
    print("Users uploaded successfully.")

def upload_all_data():
    upload_gallery_images()
    upload_posts()
    upload_users()

if __name__ == '__main__':
    upload_all_data()
