from flask import Flask,request,jsonify

app=Flask(__name__)

books = {
    1: {"title": "1984", "author": "George Orwell"},
    2: {"title": "To Kill a Mockingbird", "author": "Harper Lee"}
}
# SHOW BOOKS
@app.route("/showBooks",methods=["GET"])
def showBooks():
    return jsonify(books)

# ADD NEW BOOKS
@app.route("/addBook",methods=["POST"])
def add():
    title=request.form.get("title")
    author=request.form.get("author")
    books[len(books)+1]={"title":title,"author":author}
    return jsonify(books)

# SHOW BOOK BY ID
@app.route("/showBook/<int:id>",methods=["GET"])
def showById(id):
    if id<=len(books):
        return jsonify(books[id])
    return jsonify({"error":"book not found"})


# 




if __name__=="__main__":
    app.run(debug=True,port=3000)