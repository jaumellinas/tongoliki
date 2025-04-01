from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

URL_SUPABASE = os.getenv("URL_SUPABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = URL_SUPABASE
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

@app.route('/add_persona', methods=['GET', 'POST'])
def add_persona():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        age = request.form.get('age')
        is_trainer = request.form.get('is_trainer') == 'on'

        new_persona = Persona(
            name=name, 
            surname=surname, 
            age=int(age),
            is_trainer=is_trainer
        )

        db.session.add(new_persona)
        db.session.commit()
        return redirect(url_for('get_personas'))

    return render_template("add_persona.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)