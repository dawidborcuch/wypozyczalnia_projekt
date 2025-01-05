from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///machines.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)

def init_db():
    with app.app_context():
        db.create_all()
        if Machine.query.count() == 0:
            db.session.add(Machine(name="Koparka", price=500.0, description="Koparka gąsienicowa do prac ziemnych"))
            db.session.add(Machine(name="Walec", price=300.0, description="Walec drogowy do zagęszczania nawierzchni"))
            db.session.add(Machine(name="Dźwig", price=1000.0, description="Dźwig wieżowy do prac budowlanych"))
            db.session.commit()

@app.route('/rental')
def rental():
    machines = Machine.query.all()
    machines_list = [
        {
            "id": machine.id,
            "name": machine.name,
            "price": machine.price,
            "description": machine.description
        } for machine in machines
    ]
    return jsonify(machines_list)

@app.route('/home')
def home():
    return jsonify({
        "title": "Strona główna",
        "content": "Witamy na stronie głównej naszej wypożyczalni maszyn."
    })

@app.route('/about')
def about():
    return jsonify({
        "title": "O nas",
        "content": "Jesteśmy firmą specjalizującą się w wynajmie maszyn budowlanych, ogrodniczych i leśnych."
    })

@app.route('/contact')
def contact():
    return jsonify({
        "title": "Kontakt",
        "content": "Skontaktuj się z nami: tel. 123-456-789, email: biuro@wypozyczalnia-lochow.pl"
    })

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
