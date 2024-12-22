import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

# Configure SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'author': self.author}

# Route to test the app
@app.route("/")
def hello():
    return "Welcome to the Book Library!"

# Route to get all books (GET request)
@app.route("/getBooks", methods=["GET"])
def get_books():
    books = Book.query.all()  # Retrieve all books from the database
    return jsonify([book.to_dict() for book in books])

# # Route to add a new book (POST request)
# @app.route("/addBook", methods=["POST"])
# def add_book():
#     title = request.form.get("title")
#     author = request.form.get("author")
#     if title and author:
#         book = Book(title=title, author=author)
#         db.session.add(book)
#         db.session.commit()
#         return "Book added successfully", 201
#     return "Missing title or author", 400

# @app.route("/viewTable", methods=["GET"])
# def view_table():
#     conn = sqlite3.connect('books.db')  # Open a connection to the database
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute("SELECT * FROM books")  # Query the 'books' table
#         books = cursor.fetchall()  # Fetch all the records
#         conn.close()  # Close the connection
        
#         # Return books in a JSON response
#         return jsonify(books)
#     except sqlite3.OperationalError as e:
#         conn.close()
#         return jsonify({"error": "OperationalError: Could not fetch data from the 'books' table.", "details": str(e)})


if __name__ == "__main__":
    # Create the tables if they don't exist
    with app.app_context():
        db.create_all()  # Creates the books table if it doesn't exist already
    app.run(debug=True, port=3000)
