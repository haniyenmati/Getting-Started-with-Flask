from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
serializer_class = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
db.init_app(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'{self.name} - {self.description}'


@app.route('/')
def home():
    return "hello"


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []

    for drink in drinks:
        output.append({'id': drink.id, 'name': drink.name, 'description': drink.description})

    return jsonify(output)


@app.route('/drinks/<ID>')
def get_id(ID):
    drink = Drink.query.get_or_404(ID)
    return {'id': drink.id, 'name': drink.name, 'description': drink.description}


@app.route('/drinks', methods=['POST'])
def add_drink():
    data = request.json
    drink = Drink(name=data['name'], description=data['description'])
    db.session.add(drink)
    db.session.commit()
    return {'drink_id': drink.id}


@app.route('/drinks/<ID>', methods=["DELETE"])
def delete_drink(ID):
    drink = Drink.query.get_or_404(ID)
    db.session.delete(drink)
    db.session.commit()
    return {"msg": "done"}

@app.route('/drinks/<ID>', methods=["PUT"])
def update_drink(ID):
    data = request.json
    drink = Drink.query.get_or_404(ID)
    
    if "name" in data:
        drink.name = data['name']
    if "description" in data:
        drink.description = data['description']

    db.session.commit()

    return {"msg": "done"}

if __name__ == '__main__':
    app.run(debug=True)