import uuid
import datetime

from flask import request, render_template, redirect, jsonify
from flask_cors import cross_origin


import appdir.database as db
from appdir import app


@app.route("/books/", methods=["GET"])
@cross_origin()
def get_books():
    db.db.connect(reuse_if_open=True)
    list_of_books = []
    books = db.Book.select()
    for book in books:
        images_db = db.Image.select().where(db.Image.book_id == book.id)
        roles_db = db.Role.select(db.Role, db.Worker).where(db.Role.book_id == book.id).join(db.Worker)

        reviews_by_book = db.Review.select().where(db.Review.book_id == book.id)
        sum_score = 0
        avg = 0

        for review in reviews_by_book:
            avg += 1
            sum_score += review.score
        if avg != 0:
            score = sum_score / avg
        else:
            score = 0
        images = []
        roles = []

        for image in images_db:
            images.append({
                "image_url": image.image_url
            })

        for role in roles_db:
            roles.append({
                "role": role.role,
                "name": role.worker_id.name,
                "id": role.id
            })

        list_of_books.append({
            "id": book.id,
            "name": book.name,
            "published_year": book.published_year,
            "images": images,
            "roles": roles,
            "score": score

        })
    book_count = db.Book.select().count()
    user_count = db.User.select().count()
    publ_auth = db.Worker.select().count()

    workers_for_front = db.Worker.select()
    list_front_workers = []
    for worker in workers_for_front:
        list_front_workers.append({
            "id": worker.id,
            "name": worker.name
        })
    db.db.close()
    return render_template("MainPage.html", list_of_books=list_of_books,
                           book_count=book_count, user_count=user_count, publ_auth=publ_auth,
                           list_front_workers=list_front_workers)


@app.route("/update/<book_id>", methods=["PUT"])
@cross_origin()
def update_book(book_id):
    db.db.connect(reuse_if_open=True)
    data = request.get_json()
    book = db.Book.get_or_none(db.Book.id==book_id)
    if book:
        book.name = data["name"]
        book.published_year = data["published_year"]
        book.save()
        db.Role.delete().where(db.Role.book_id==book_id).execute()
        roles = [
        {
            "book_id": book_id,
            "worker_id": data["publisher"],
            "role": "publisher"
        },
        {
            "book_id": book_id,
            "worker_id": data["author"],
            "role": "author"
        }
        ]
        db.Role.insert_many(roles).on_conflict_ignore().execute()
    db.db.close()
    return jsonify({"success": True, "message": "Book updated successfully"})


@app.route("/delete/<book_id>", methods=["DELETE"])
@cross_origin()
def delete_book(book_id):
    db.db.connect(reuse_if_open=True)
    book = db.Book.get_or_none(db.Book.id==book_id)
    if book:
        db.Review.delete().where(db.Review.book_id==book_id).execute()
        db.Image.delete().where(db.Image.book_id==book_id).execute()
        db.Role.delete().where(db.Role.book_id==book_id).execute()
        db.Book.delete().where(db.Book.id==book_id).execute()
        db.db.close()
        return jsonify({"success": True, "message": "Book deleted successfully"})
    else:
        db.db.close()
        return jsonify({"success": True, "message": "Book deleted successfully"})


@app.route("/create/book", methods=["POST"])
@cross_origin()
def create():
    data = request.get_json()
    print(data)
    id = uuid.uuid4()
    year = data['publishedYear'].split("-")[-1]
    book = {
        "id": id,
        "name": data['bookName'],
        "published_year": year
    }
    image = {
        "book_id": id,
        "image_url": data["imageUrl"]
    }
    roles = [
        {
            "book_id": id,
            "worker_id": data["publisherId"],
            "role": "publisher"
        },
        {
            "book_id": id,
            "worker_id": data["authorId"],
            "role": "author"
        }

    ]
    db.db.connect(reuse_if_open=True)
    db.Book.insert(book).execute()
    db.Role.insert_many(roles).on_conflict_ignore().execute()
    db.Image.insert(image).execute()
    db.db.close()
    return jsonify({"success": True, "message": "Book added successfully"})


@app.route("/book/<book_id>")
def get_review(book_id):
    reviews = []
    images = []
    roles = []
    db.db.connect(reuse_if_open=True)
    book = db.Book.get_or_none(db.Book.id==book_id)
    if book:
        selected = {}
        workers_for_front = db.Worker.select()
        list_front_workers = []
        for worker in workers_for_front:
            list_front_workers.append({
                "id": worker.id,
                "name": worker.name
            })
        images_db = db.Image.select().where(db.Image.book_id==book_id)
        reviews_from_db = db.Review.select(db.Review, db.User).where(db.Review.book_id==book_id).join(db.User)
        users_for_reviews = db.User.select()
        user_list = []
        for user_review in users_for_reviews:
            user_list.append({
                "username": user_review.username,
                "id": user_review.id
            })
        for review in reviews_from_db:
            reviews.append({
                "id": review.id,
                "username": review.user_id.username,
                "score": review.score,
                "description": review.description
            })
        roles_db = db.Role.select(db.Role, db.Worker).where(db.Role.book_id == book.id).join(db.Worker)
        for role in roles_db:
            selected[f"{role.role}"] = role.id
            roles.append({
                "role": role.role,
                "name": role.worker_id.name,
                "id": role.id
            })
        for image in images_db:
            images.append({
                "url": image.image_url
            })
        end_dict ={
            "name": book.name,
            "year": book.published_year,
            "id": book.id,
            "images": images,
            "reviews": reviews,
            "roles": roles
        }
        db.db.close()
        return render_template("homeWork/homeWork.html", end_dict=end_dict, user_list=user_list,
                               list_front_workers=list_front_workers, selected=selected)
    else:
        db.db.close()
        return 404


@app.route("/create/review", methods=["POST"])
@cross_origin()
def create_review():
    data = request.get_json()
    print(data)
    review = {
        "book_id": data["bookId"],
        "user_id": data["userId"],
        "score": data["rating"],
        "description": data["description"]
    }
    db.db.connect(reuse_if_open=True)
    db.Review.insert(review).execute()
    db.db.close()
    return jsonify({"success": True, "message": "Review added successfully"})


@app.route("/create/worker", methods=["POST"])
@cross_origin()
def create_worker():
    data = request.get_json()
    print(data)
    worker = {
        "name": data["name"]
    }
    db.Worker.insert(worker).execute()
    return jsonify({"success": True, "message": "Worker added successfully"})


@app.route("/create/user", methods=["POST"])
@cross_origin()
def create_user():
    data = request.get_json()
    user_count = db.User.select().count()
    current_datetime = datetime.datetime.now()
    print(data)
    user = {
        "username": data["username"],
        "mail": data["email"],
        "id": int(user_count) + 1,
        "creation_date": current_datetime.strftime('%Y-%m-%d')
    }
    db.User.insert(user).execute()
    return jsonify({"success": True, "message": "User added successfully"})