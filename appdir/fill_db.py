import random

import pandas as pd

from mimesis import Generic
from mimesis.locales import Locale

import appdir.database as db


def fill_books():
    list_of_books, list_of_workers = [], []
    counter = 0
    for chunk in pd.read_csv("books.csv", delimiter=";", encoding="ISO-8859-1", chunksize=50):
        for index, row in chunk.iterrows():
            list_of_books.append({
                "id": row["ISBN"],
                "name": row["Book-Title"],
                "published_year": row["Year-Of-Publication"]
            })
            list_of_workers.append({
                "name": row["Publisher"]
            })
            list_of_workers.append({
                "name": row["Book-Author"]
            })
        counter += 50
        print(len(chunk["ISBN"]))
        if counter >= 500:
            break
    db.db.connect(reuse_if_open=True)
    db.Book.insert_many(list_of_books).on_conflict(conflict_target=[db.Book.id],
                                                   preserve=[db.Book.name,
                                                             db.Book.published_year]).execute()
    db.Worker.insert_many(list_of_workers).on_conflict_ignore().execute()
    db.db.close()

    list_of_chains, list_of_images = [], []
    db.db.connect(reuse_if_open=True)
    counter = 0
    for chunk in pd.read_csv("books.csv", delimiter=";", encoding="ISO-8859-1", chunksize=50):
        for index, row in chunk.iterrows():
            publisher = db.Worker.get_or_none(db.Worker.name == row["Publisher"])
            author = db.Worker.get_or_none(db.Worker.name == row["Book-Author"])
            if publisher:
                list_of_chains.append({
                    "book_id": row["ISBN"],
                    "worker_id": publisher.id,
                    "role": "publisher"
                })
            if author:
                list_of_chains.append({
                    "book_id": row["ISBN"],
                    "worker_id": author.id,
                    "role": "author"
                })
            list_of_images.append({
                "book_id": row["ISBN"],
                "image_url": row["Image-URL-L"]
            })
        counter += 50
        print(len(chunk["ISBN"]))
        if counter >= 500:
            break
    db.Role.insert_many(list_of_chains).on_conflict_ignore().execute()
    db.Image.insert_many(list_of_images).on_conflict_ignore().execute()
    db.db.close()
    return True


def fill_users(num_users=500):
    generic = Generic(Locale.RU)
    list_of_users = []
    for i in range(num_users):
        list_of_users.append({
            "id": i,
            "mail": generic.person.email(),
            "username": generic.person.username(),
            "creation_date": generic.datetime.date()
        })
    db.db.connect(reuse_if_open=True)
    db.User.insert_many(list_of_users).on_conflict(conflict_target=[db.User.id],
                                                   preserve=[db.User.mail,
                                                             db.User.username,
                                                             db.User.creation_date]).execute()
    db.db.close()
    return True


def fill_reviews(num_reviews=1000):
    generic = Generic(Locale.RU)

    user_ids = [user.id for user in db.User.select()]
    book_ids = [book.id for book in db.Book.select()]

    list_of_reviews = []
    for _ in range(num_reviews):
        list_of_reviews.append({
            "book_id": random.choice(book_ids),
            "user_id": random.choice(user_ids),
            "score": random.randint(1, 5),
            "description": generic.text.text()
        })
    db.db.connect(reuse_if_open=True)
    db.Review.insert_many(list_of_reviews).on_conflict_ignore().execute()
    db.db.close()
    return True