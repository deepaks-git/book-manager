import os
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from flasgger import Swagger

app=Flask(__name__)
Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///finalBook.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY']='secret_key'

db=SQLAlchemy(app)
jwt=JWTManager(app)

# USER MODEL
class User(db.Model):
    username=db.Column(db.String(80),primary_key=True)
    password=db.Column(db.String(80),nullable=False)
    """
    Represents a user in the system.

    Attributes:
    username (str): The unique username of the user. (Primary key)
    password (str): The hashed password for authentication.
    """

# BOOK MODEL
class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80),nullable=False)
    author=db.Column(db.String(80),nullable=False)
    
    def to_dict(self):
        return {'id':self.id,'title':self.title,'author':self.author}

# WELCOME MESSAGE
@app.route("/")
@jwt_required()
def welcome():
    """
    Welcome Endpoint
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
    description: Bearer token for authorization
    responses:
      200:
        description: Welcome to Books Library
    """
    return "Welcome to Books Library"

# LOGIN USERS 
@app.route("/login",methods=["POST"])
def login():
    """
    Login Endpoint
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      200:
        description: JWT Token
    """
    username=request.form.get("username")
    password=request.form.get("password")
    user=User.query.filter_by(username=username,password=password).first()
    if user:
        access_token=create_access_token(identity=user.username)
        return jsonify(access_token=access_token)
    return "Not valid user "

# ADD NEW BOOKS
@app.route("/addBook",methods=["POST"])
@jwt_required()
def addBook():
    """
    Add a New Book
    ---
    parameters:
      - name: title
        in: formData
        type: string
        required: true
      - name: author
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Book added successfully
      400:
        description: Title and Author fields are empty
    """
    title=request.form.get("title")
    author=request.form.get("author")
    if title and author:
        book=Book(title=title,author=author)
        db.session.add(book)
        db.session.commit()
        return "added successfully",200
    return "Title and Author feild empty",400

# UPDATE BOOK BY ID
@app.route("/updateBook/<int:id>",methods=["PUT"])
@jwt_required()
def updateBook(id):
    """
    Update Book by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: title
        in: formData
        type: string
        required: true
      - name: author
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Book updated successfully
      404:
        description: Book not found
    """
    book=Book.query.get(id)
    title=request.form.get("title")
    author=request.form.get("author")
    if not book:
        return "Book not found!",404
    if not author or not title:
        return "author and title feild is empty",400
    book.title=title
    book.author=author
    db.session.commit()
    return "Book updated",200

# DELETE BOOK BY ID
@app.route("/deleteBook/<int:id>",methods=["DELETE"])
@jwt_required()
def deleteBook(id):
    """
    Delete Book by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Book deleted successfully
      404:
        description: Book not found
    """
    book=Book.query.get(id)
    if not book:
        return "Book not found!",404
    db.session.delete(book)
    db.session.commit()
    return "Book deleted",200

# VIEW BOOKS
@app.route("/showBooks",methods=["GET"])
def showBooks():
    """
    View Books with Pagination
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
      - name: limit
        in: query
        type: integer
        required: false
    responses:
      200:
        description: List of books
    """
    # PAGINATION
    page=int(request.args.get('page',1))
    limit=int(request.args.get('limit',5))
    offset=(page-1)*limit
    # pagination ends

    books=Book.query.offset(offset).limit(limit).all()
    return jsonify([ book.to_dict() for book in books ])

# SORT BOOKS
@app.route("/books/sort", methods=["GET"])
def get_sorted_books():
    """
    Sort Books
    ---
    parameters:
      - name: sort_by
        in: query
        type: string
        required: false
      - name: order
        in: query
        type: string
        required: false
    responses:
      200:
        description: Sorted list of books
    """
    sort_by = request.args.get("sort_by", "title")  # Default to sorting by title
    order = request.args.get("order", "asc")  # Default to ascending order

    if order == "desc":
        books = Book.query.order_by(db.desc(getattr(Book, sort_by))).all()
    else:
        books = Book.query.order_by(getattr(Book, sort_by)).all()

    return jsonify([book.to_dict() for book in books])

# FILTER BOOKS
@app.route("/books/filter", methods=["GET"])
def get_filtered_books():
    """
    Filter Books
    ---
    parameters:
      - name: author
        in: query
        type: string
        required: false
      - name: title
        in: query
        type: string
        required: false
    responses:
      200:
        description: Filtered list of books
    """
    author = request.args.get("author")  # Filter by author
    title = request.args.get("title")  # Filter by title (optional)

    query = Book.query
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    books = query.all()
    return jsonify([book.to_dict() for book in books])

# START THE APP ALONG WITH THE DATABASE
if __name__=="__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True,port=3000)
