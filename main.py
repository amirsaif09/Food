from flask import Flask, request, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_cors import cross_origin


custom_html_path = r'E:\projects\kuchbhi-main\kuchbhi-main'

app = Flask(__name__)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    restaurant = db.Column(db.String(50))
    food = db.Column(db.String(50))
    rating = db.Column(db.String(6))
    comment = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'restaurant': self.restaurant,
            'food': self.food,
            'rating': self.rating,
            'comment': self.comment
        }

# Create the tables (this will create database.db automatically)
with app.app_context():
    db.create_all()




@app.route("/")
def Home():
    row_review = User.query.all()
    users_data = [r.to_dict() for r in row_review]
    # review = jsonify(users_data)
    return render_template('index.html',review=users_data)

@app.route('/review',methods=['POST'])
@cross_origin()
def review():
    # Add a user if table is empty
    name = request.form.get('name1')  # text
    restaurant = request.form.get('restaurant') 
    food = request.form.get('food') # text
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    db.session.add(User(name=name,restaurant=restaurant,food=food,rating=rating,comment=comment))
    db.session.commit()
    data = User.query.all()
    users_data = [r.to_dict() for r in data]

    
    return {"status":200,"review":users_data}

@app.route("/<string:page_name>")
def otherpages(page_name):
    print(page_name,'this is slug')
    return render_template(f'{page_name}')
        


if __name__ == '__main__':
    app.run(debug=True)