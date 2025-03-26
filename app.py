from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)    
    surname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    is_trainer = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return f'Persona {self.name}'
    
    
@app.route('/')
def get_index():
    return render_template("index.html")    
    
@app.route('/personas')
def get_personas():
    personas = Persona.query.all()
    return render_template("personas.html", personas = personas)


@app.route('/add_persona/<name>/<surname>/<age>/<is_trainer>')
def add_user(name, surname, age, is_trainer):
    is_trainer = request.args.get('is_trainer', 'False')  # Obtiene el valor como string (por defecto 'False')
    is_trainer = is_trainer.lower() == 'true'  # Convierte 'True'/'False' a booleano

    new_persona = Persona(name=name, surname=surname, age=age, is_trainer=is_trainer)
    db.session.add(new_persona)
    db.session.commit()
    return f"{name} añadido correctamente."


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)