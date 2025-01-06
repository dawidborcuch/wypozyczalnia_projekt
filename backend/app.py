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
    category = db.Column(db.String(50), nullable=False)

def init_db():
    with app.app_context():
        db.create_all()
        print("Baza danych została utworzona.")

@app.route('/rental')
def rental():
    return jsonify({
        "title": "Wynajem maszyn",
        "content": "Wybierz kategorię maszyn, aby zobaczyć dostępne opcje."
    })

@app.route('/rental/all')
def rental_all():
    try:
        machines = Machine.query.all()
        print(f"Znaleziono {len(machines)} maszyn. Pierwsza to {machines[0]}")
        machines_list = [
            {
                "id": machine.id,
                "name": machine.name,
                "price": machine.price,
                "description": machine.description,
                "category": machine.category
            } for machine in machines
        ]
        return jsonify(machines_list)
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")
        return jsonify({"error": "Wystąpił błąd podczas pobierania danych"}), 500


@app.route('/rental/<category>')
def rental_category(category):
    category_mapping = {
        'construction': '1',
        'garden': '2',
        'trailers': '3'
    }
    db_category = category_mapping.get(category, category)

    machines = Machine.query.filter_by(category=db_category).all()
    print(f"Znaleziono {len(machines)} maszyn dla kategorii {category} (DB category: {db_category})")
    machines_list = [
        {
            "id": machine.id,
            "name": machine.name,
            "price": machine.price,
            "description": machine.description,
            "category": machine.category
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
