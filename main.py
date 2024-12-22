import os
from flask import Flask,request,jsonify

app=Flask(__name__)

books={
  1:{"title":"naruto", "author":"sheepu"},
  2:{"title":"gow", "author":"godyy"}

}

@app.route("/")
def welcome():
  return "Welcome to book manager"

@app.route("/showBooks")
def showBooks():
  return books

@app.route("/addBook",methods=["GET","POST"])
def addBook():

  title=request.form.get("title")
  author=request.form.get("author")
  if title and author:
    books[len(books)+1]={"title":title,"author":author}
    return jsonify(books),200
  return "not added"

    # get post put delete
  
@app.route("/showBook/<int:id>")
def showBookById(id):
  return books[id]


@app.route("/updateBook/<int:id>",methods=["PUT"])
def updateBook(id):
  title=request.form.get("title")
  author=request.form.get("author")
  if title and author:
    books[id]={"title":title,"author":author}
    return jsonify(books),200
  return "not updated"

@app.route("/deleteBook/<int:id>",methods=["DELETE"])
def deleteBook(id):
  if id in books:
    del books[id]
    return jsonify(books),200
  return "not deleted"






if __name__=="__main__" :
  app.run(debug=True,port=3000)