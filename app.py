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

@app.route("/")
def root():
    return render_template("base.html")

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Lists all cupcakes

        response should look like:
        "cupcakes": [
                    {
                    "id": 1, 
                    "flavor": "chocolate", 
                    "size": "small", 
                    "rating": 10, 
                    "image": "imageurl.com"
                    }, 

                    {
                    "id": 1, 
                    "flavor": "chocolate", 
                    "size": "small", 
                    "rating": 10, 
                    "image": "imageurl.com"
                    }]
    """
    # example of response data in docstring
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake_details(cupcake_id):
    """Shows the details of a specific cupcake
    
        response should look like:

        {cupcake: 
            {"id": 1, 
            "flavor": "chocolate", 
            "size": "small", 
            "rating": 10, 
            "image": "imageurl.com"}
        }
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a new cupcake with input from user
    
        input should look like:

        {"flavor": "chocolate", 
         "size": "small", 
         "rating": 10, 
         "image": "imageurl.com"}
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


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ updates a cupcake with specified ID - input should be json of 
        attributes of cupcake to be changed

        input should look like: 

        {
            "flavor":"raspberry",
            "size":"small",
            "rating":10,
            "image":"your_image_url"
        }

        changes made are to object attributes and returns this:

            {
            "cupcake": {
                        "flavor": "raspberry",
                        "id": 3,
                        "image": "your_image_url",
                        "rating": 10,
                        "size": "small"
                       }
            }
    """

    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data["flavor"]
    cupcake.size = data["size"]
    cupcake.rating = data["rating"]
    cupcake.image = data["image"]
    

    db.session.commit()
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Deletes cupcake with specified cupcake ID or returns
        404 if cupcake not found """
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)

    db.session.commit()
    return jsonify(message="Deleted")

    