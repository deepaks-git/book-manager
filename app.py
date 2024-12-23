import os
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from flasgger import Swagger
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import timedelta


app=Flask(__name__)


# Add a description or instructions for using the API
app.config['SWAGGER'] = {
    'title': 'Shelf-Master API',
    'description': '''
    API Usage Steps:
    1. Register an account by posting to `/register` with a username and password.
    2. Login by posting to `/login` with your credentials to get a JWT token.
    3. Use the JWT token in the Authorization header as `Bearer <your_token>` for all API requests.
    
    Please use the Bearer token to authenticate your requests.
    ''',
    'uiversion': 3,
    'termsOfService': '/static/terms.html'
    
    
}

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///finalBook.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY']='itz_dee8'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(hours=1)

db=SQLAlchemy(app)
jwt=JWTManager(app)
swagger= Swagger(app)
# USER MODEL
class User(db.Model):
    username=db.Column(db.String(80),primary_key=True)
    password=db.Column(db.String(80),nullable=False)


    

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
    WELCOME ENDPOINT
    ---
    parameters:
        -   name: Authorization
            in: header
            type: string
            required: true
    description: Enter the authorization token to access this endpoint

    responses:
        200:
            description: Welcome
        
    """
    return "Welcome to Books Library"


# LOGIN USERS 
@app.route("/login",methods=["POST"])
def login():
    """
    LOGIN ENDPOINT
    ---
    parameters:
        -   name: username
            in: formData
            type: string
            required: true
        -   name: password
            in: formData
            type: string
            required: true
    responses:
        200:
            description: JWT Token
        400:
            description: Invalid credentials
    """
    username=request.form.get("username")
    password=request.form.get("password")
    
    user=User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token=create_access_token(identity=user.username)
        return jsonify(access_token=access_token)
    return "Not valid user "

# REGISTER USER
@app.route("/register",methods=["POST"])
def register():
    """
    REGISTER ENDPOINT
    ---
    parameters:
        -   name: username
            in: formData
            type: string
            required: true
        -   name: password
            in: formData
            type: string
            required: true
    responses:
        200:
            description: User id created successfully, head over to /login to generate your token
        400:
            description: User not created or user already exists
    """
    username=request.form.get("username").lower()
    password=request.form.get("password")
    user=User.query.get(username)
    if user:
        return "user already exists",400
    
    if username and password:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user=User(username=username,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return "user id created successfully, head over to /login to generate your token",200
    return "user not created"

# ADD NEW BOOKS
@app.route("/addBook",methods=["POST"])
@jwt_required()
def addBook():
    """
    ADD A BOOK
    ---
    parameters:
        -   name: title
            in: formData
            type: string
            required: yes
        -   name: author
            in: formData
            type: string
            required: true
        -   name: Authorization
            in: header
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
        return "added successfully",201
    return "Title and Author feild empty",500

# UPDATE BOOK BY ID
@app.route("/updateBook/<int:id>",methods=["PUT"])
@jwt_required()
def updateBook(id):
    """
    UPDATE BOOKS
    ---
    parameters:
        -   name: id
            in: path
            type: integer
            required: true
        -   name: title
            in: formData
            type: string
            required: true
        -   name: author
            in: formData
            type: string
            required: true
        -   name: authorization
            in: header
            type: string
            required: true

    responses:
        200:
            description: Book updated successfully
        404:
            description: Book not found
        400:
            description: Author and Title fields are empty

    """
    book=Book.query.get(id)
    title=request.form.get("title")
    author=request.form.get("author")
    if not book:
        return "Book not found!",404
    if not author or not title:
        return "author and title feild is empty"
    book.title=title
    book.author=author
    db.session.commit()
    return "Book updated",200

# DELETE BOOK BY ID
@app.route("/deleteBook/<int:id>",methods=["DELETE"])
@jwt_required()
def deleteBook(id):
    """
    DELETE BOOK ENDPOINT
    ---
    parameters:
        -   name: id
            in: path
            type: integer
            required: true
        -   name: authorization
            in: header
            type: string
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
    VIEW BOOKS
    ---
    parameters:
        -   name: authorization
            in: header
            type: string
            required: true
        -   name: page
            in: query
            type: integer
            required: false
        -   name: limit
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
    total_books = Book.query.count()
    # pagination ends

    books=Book.query.offset(offset).limit(limit).all()
    print("LIST OF BOOKS")
    return jsonify({
        "Current_Page":page,
        "Limit" : limit,
        "Total Books" : total_books,
        "Books":[ book.to_dict() for book in books ]})



# SORT BOOKS
@app.route("/books/sort", methods=["GET"])
@jwt_required()
def get_sorted_books():
    """
    SORT BOOKS ENDPOINT
    ---
    parameters:
        -   name: sort_by
            in: query
            type: string
            required: false
        -   name: order
            in: query
            type: string
            required: false
        -   name: authorization
            in: header
            type: string
            required: true
    responses:
        200:
            description: Sorted list of books
        500:
            description: Invalid sort by or order feild. sort by(title/author), order(asc/desc)
    """
    sort_by = request.args.get("sort_by", "title")  # Default to sorting by title
    order = request.args.get("order", "asc")  # Default to ascending order
    if sort_by not in ["title", "author"] or order not in ["asc", "desc"]:
        return jsonify({"error": "Invalid sort_by or order field. sort_by (title/author), order (asc/desc)"}), 400


    if order == "desc":
        books = Book.query.order_by(db.desc(getattr(Book, sort_by))).all()
    else:
        books = Book.query.order_by(getattr(Book, sort_by)).all()

    return jsonify([book.to_dict() for book in books])

# FILTER BOOKS
@app.route("/books/filter", methods=["GET"])
@jwt_required()
def get_filtered_books():
    """
    FILTER BOOKS ENDPOINT
    ---
    parameters:
        -   name: author
            in: query
            type: string
            required: false
        -   name: title
            in: query
            type: string
            required: false
        -   name: authorization
            in: header
            type: string
            required: true
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