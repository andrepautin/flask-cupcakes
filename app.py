"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Lists all cupcakes

        response should look like:
        [{"id": 1, 
        "flavor": "chocolate", 
        "size": "small", 
        "rating": 10, 
        "image": "imageurl.com"}, 

        {"id": 1, 
        "flavor": "chocolate", 
        "size": "small", 
        "rating": 10, 
        "image": "imageurl.com"}]
    """
    # example of response data in docstring
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake_details(cupcake_id):
    """Shows the details of a specific cupcake
    
        response should look like:

        {"id": 1, 
        "flavor": "chocolate", 
        "size": "small", 
        "rating": 10, 
        "image": "imageurl.com"}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a new cupcake with input from user
    
    
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()
    serialized = cupcake.serialize()
    
    return (jsonify(cupcake=serialized), 201)
