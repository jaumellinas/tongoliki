from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)

load_dotenv()

URL_SUPABASE = os.getenv("URL_SUPABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = URL_SUPABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)    
    surname = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100), nullable=True)
    number = db.Column(db.Integer(), nullable=True)
    position = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=True)
    dominant_leg = db.Column(db.String(100), nullable=True)
    is_international = db.Column(db.Boolean, nullable=False)
    is_trainer = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return f'Persona {self.name}'

class Partido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    local_team_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    visitor_team_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(5), nullable=False)

    local_team = db.relationship('Equipo', foreign_keys=[local_team_id], backref='partidos_local')
    visitor_team = db.relationship('Equipo', foreign_keys=[visitor_team_id], backref='partidos_visitantes')

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(3), nullable=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), nullable=False)
    identificador = db.Column(db.String(100), nullable=False)

@app.route('/')
def get_index():
    personas = Persona.query.all()
    partidos = Partido.query.order_by(Partido.date.asc()).all()
    sponsors = os.listdir('static/img/sponsors')
    return render_template("index.html", personas = personas, partidos = partidos, sponsors = sponsors)

@app.route('/personas')
def get_personas():
    personas = Persona.query.all()
    return render_template("players/personas.html", personas = personas)

@app.route('/admin', methods=["GET", "POST"])
def get_personas_admin():
    tipo = request.args.get("tipo", "personas")  # Usa 'personas' como valor por defecto
    personas = Persona.query.all()
    equipos = Equipo.query.all()
    partidos = Partido.query.all()
    videos = Video.query.all()
    return render_template("admin/admin_panel.html", tipo=tipo, personas=personas, equipos=equipos, partidos=partidos, videos=videos)

@app.route('/editar_persona/<int:id>', methods=['GET', 'POST'])
def editar_persona(id):
    persona = Persona.query.get(id)
    if not persona:
        return "Usuario no encontrado", 404
    if request.method == 'POST':
        persona.name = request.form.get('name')
        persona.surname = request.form.get('surname')
        persona.age = int(request.form.get('age'))
        persona.is_trainer = request.form.get('is_trainer')     == 'on'
        db.session.commit()
        return redirect(url_for('get_personas_admin'))
    
    return render_template("edit/editar_persona.html", persona = persona)

@app.route('/persona/<int:id>', methods=['GET', 'POST'])
def get_persona_by_id(id):
    persona = Persona.query.get(id)
    if not persona:
        return "Persona no encontrada", 404
    else:
        return render_template("players/datos_jugador.html", persona = persona)
        

@app.route('/borrar_persona/<int:id>', methods=['GET', 'POST'])
def borrar_persona(id):
    persona = Persona.query.get(id)
    if not persona:
        return "Persona no encontrada", 404
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('get_personas_admin'))

@app.route('/add_persona', methods=['GET', 'POST'])
def add_persona():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        display_name = request.form.get('display_name')
        number = int(request.form.get('number')) if request.form.get('number') else None
        position = request.form.get('position')
        dob = datetime.strptime(request.form.get('dob'), "%Y-%m-%d").date()
        birthplace = request.form.get('birthplace')
        nationality = request.form.get('nationality')
        dominant_leg = request.form.get('dominant_leg')
        is_international = request.form.get('is_international') == 'on'
        is_trainer = request.form.get('is_trainer') == 'on'
        
        new_persona = Persona(
            name=name,
            surname=surname,
            display_name=display_name,
            number=number,
            position=position,
            dob=dob,
            birthplace=birthplace,
            nationality=nationality,
            dominant_leg=dominant_leg,
            is_international=is_international,
            is_trainer=is_trainer
        )
        
        db.session.add(new_persona)
        db.session.commit()
        return redirect(url_for('get_personas_admin'))

    return render_template("add/add_persona.html")

@app.route('/add_partido', methods=['GET', 'POST'])
def add_partido():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        local_team_id = request.form.get('local_team_id')
        visitor_team_id = request.form.get('visitor_team_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = time_str

        new_partido = Partido(
            name=name,
            location=location,
            local_team_id=local_team_id,
            visitor_team_id=visitor_team_id,
            date=date,
            time=time,
        )

        db.session.add(new_partido)
        db.session.commit()
        return redirect(url_for('get_personas_admin'))

    return render_template("add/add_partido.html")

@app.route('/add_equipo', methods=['GET', 'POST'])
def add_equipo():
    if request.method == 'POST':
        name = request.form.get('name')
        abbreviation = request.form.get('abbreviation')

        new_equipo = Equipo(
            name=name,
            abbreviation=abbreviation,
        )

        db.session.add(new_equipo)
        db.session.commit()
        return redirect(url_for('get_personas_admin'))

    return render_template("add/add_equipo.html")


@app.route('/forms')
def get_forms():
    tipo = request.args.get("tipo", None)      
    equipos = Equipo.query.all()
    personas = Persona.query.all()
    partidos = Partido.query.all()
    videos = Video.query.all()
    return render_template("components/forms.html", tipo=tipo, personas=personas, equipos=equipos, partidos=partidos, videos=videos)

@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == "POST":
        email_get = request.form.get('email')
        password_get = request.form.get('password')
        correo = "tongoliki@gmail.com"
        contraseña = "12345"
        if email_get == correo and password_get == contraseña:
            return redirect(url_for('get_personas_admin'))
        
    return render_template("auth/login.html")

@app.route('/editar_equipo/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    if request.method == 'POST':
        equipo.name = request.form.get('name')
        equipo.abbreviation = request.form.get('abbreviation')
        db.session.commit()
        return redirect(url_for('get_personas_admin', tipo='equipos'))
    return render_template('edit/editar_equipo.html', equipo=equipo)

# Ruta para borrar Equipo
@app.route('/borrar_equipo/<int:id>', methods=['POST'])
def borrar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    return redirect(url_for('get_personas_admin', tipo='equipos'))

@app.route('/editar_partido/<int:id>', methods=['GET', 'POST'])
def editar_partido(id):
    partido = Partido.query.get(id)
    if not partido:
        return "Partido no encontrado", 404

    if request.method == 'POST':
        partido.name = request.form.get('name')
        partido.location = request.form.get('location')
        partido.local_team_id = request.form.get('local_team_id')
        partido.visitor_team_id = request.form.get('visitor_team_id')
        partido.date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
        partido.time = request.form.get('time')
        db.session.commit()
        return redirect(url_for('get_personas_admin', tipo='partidos'))

    equipos = Equipo.query.all()
    return render_template('edit/editar_partido.html', partido=partido, equipos=equipos)


# --- BORRAR PARTIDO ---
@app.route('/borrar_partido/<int:id>', methods=['POST'])
def borrar_partido(id):
    partido = Partido.query.get(id)
    if not partido:
        return "Partido no encontrado", 404
    db.session.delete(partido)
    db.session.commit()
    return redirect(url_for('get_personas_admin', tipo='partidos'))


# --- EDITAR VIDEO ---
@app.route('/editar_video/<int:id>', methods=['GET', 'POST'])
def editar_video(id):
    video = Video.query.get(id)
    if not video:
        return "Vídeo no encontrado", 404

    if request.method == 'POST':
        video.url = request.form.get('url')
        video.identificador = request.form.get('identificador')
        db.session.commit()
        return redirect(url_for('get_personas_admin', tipo='videos'))

    return render_template('edit/editar_video.html', video=video)


# --- BORRAR VIDEO ---
@app.route('/borrar_video/<int:id>', methods=['POST'])
def borrar_video(id):
    video = Video.query.get(id)
    if not video:
        return "Vídeo no encontrado", 404
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('get_personas_admin', tipo='videos'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)