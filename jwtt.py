import os
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config['JWT_SECRET_KEY']='secretkey'

db=SQLAlchemy(app)
jwt=JWTManager(app)

class User(db.Model):
    username=db.Column(db.String(80),primary_key=True)
    password=db.Column(db.String(80),nullable=False)

    def to_dict(self):
        return {"username":self.username,"password":self.password}

@app.route("/login",methods=["POST"])
def login():
    username=request.json.get("username")
    password=request.json.get("password")
    user=User.query.filter_by(username=username, password=password).first()
    if user:
        access_token=create_access_token(identity=user.username)
        return jsonify(access_token=access_token)
    return "invalid credentials"


@app.route("/test",methods=["GET"])
@jwt_required()
def getUsers():
    users=User.query.all()
    return jsonify([user.to_dict() for user in users])


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=3000)
