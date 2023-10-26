from blog.database import mongo
import pymongo
from datetime import datetime
from unidecode import unidecode   
from werkzeug.exceptions import Conflict

def generate_slug(title: str) -> str:
    return unidecode(title).replace(" ", "-").replace("_", "-").lower()

def get_all_posts(published: bool = True):
    posts = mongo.db.posts.find({"published": published})
    return posts.sort("date", pymongo.DESCENDING) 
    

def get_post_by_slug(slug: str) -> dict:
    post = mongo.db.posts.find_one({"slug": slug})
    return post
    

def update_post_by_slug(slug: str, data: dict, published: bool = None) -> dict:
    if "title" in data:
        new_slug = generate_slug(data["title"])        
        
        existing_post = mongo.db.posts.find_one({"slug": new_slug})
        if existing_post and existing_post['slug'] != slug:
            raise Conflict("A post with this slug already exists.")
        
        data["slug"] = new_slug
    
    if published is not None:
        data["published"] = published    
    
    data["date"] = datetime.now()
        
    return mongo.db.posts.find_one_and_update({"slug": slug}, {"$set": data}, return_document=True)


def new_post(title: str, content: str, published: bool = True) -> str:
    slug = generate_slug(title)
    existing_post = mongo.db.posts.find_one({"slug": slug})
    if existing_post:
        raise Conflict("A post with this slug already exists.")
    mongo.db.posts.insert_one(
        {
            "title": title,
            "content": content,
            "slug": slug,
            "published": published,
            "date": datetime.now()
        }
    )
    return slug
