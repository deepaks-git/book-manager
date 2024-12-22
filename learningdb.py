import os
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)

# API Key for Authentication
API_KEY = "itzdee8"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(80),nullable=False)
    author=db.Column(db.String(80),nullable=False)

    def to_dict(self):
        return {'id':self.id,'title':self.title,'author':self.author}


# Middleware to Validate API Key
def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')  # Look for API key in headers
        if api_key != API_KEY:
            return jsonify({'error': 'Unauthorized access'}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route("/")
def welcome():
    return "Welcome to Book Library"

@app.route("/getBooks",methods=["GET"])
def getBooks():
    books=Book.query.all()
    return jsonify([book.to_dict() for book in books])

@app.route("/addBook",methods=["POST"])
@require_api_key  # Protect this route
def addBook():
    title=request.form.get("title")
    author=request.form.get("author")
    if title and author:
        book=Book(title=title,author=author)
        db.session.add(book)
        db.session.commit()
        return "book added successfully",201
    return "no title or author to add",500

@app.route("/updateBook/<int:id>",methods=["PUT"])
def updateBook(id):	
	book=Book.query.get(id)
	title=request.form.get("title")
	author=request.form.get("author")
	if title and author and book:
		book.title=title
		book.author=author
		db.session.commit()
		return "book updated successfully"
	return "either book not found sqliteor empty inputs"



@app.route("/deleteBook/<int:id>",methods=["DELETE"])
def deleteBook(id):
    book=Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return "book deleted successfully"
    return "no books with that id found"

    
    

if __name__=="__main__":

    with app.app_context():
        db.create_all()



    app.run(debug=True,port=3000)
