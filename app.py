from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)

load_dotenv()

URL_SUPABASE = os.getenv("URL_SUPABASE")

app.config['SQLALCHEMY_DATABASE_URI'] = URL_SUPABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY")
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

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    collection = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    in_cart = db.Column(db.Boolean, nullable=True)
    in_promo = db.Column(db.Boolean, nullable=True)
    qty = db.Column(db.Integer, default=1)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Promo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.Integer, nullable=False)

@app.route('/')
def get_index():
    personas = Persona.query.filter_by(is_trainer=False).order_by(Persona.number.asc()).all()
    partidos = Partido.query.order_by(Partido.date.asc()).limit(3).all()
    sponsors = os.listdir('static/img/sponsors')
    videos = Video.query.order_by(Video.id.desc()).limit(4).all()
    return render_template("index.html", personas = personas, partidos = partidos, sponsors = sponsors, videos = videos)

@app.route('/plantilla')
def get_plantilla():
    personas = Persona.query.all()
    return render_template("players/plantilla.html", personas = personas)

@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == "POST":
        email_get = request.form.get('email')
        password_get = request.form.get('password')

        user = Usuario.query.filter_by(mail=email_get, password=password_get).first()

        if user:
            if user: 
                session['user_login'] = True
                if user.is_admin:
                    session['is_admin'] = user.is_admin
                    return redirect(url_for('get_choice'))
                else:
                    return redirect(url_for('mostrar_inicio'))
        else:
            return render_template("auth/login.html", error="badlogin")
        
    return render_template("auth/login.html")

@app.route('/choice', methods=['GET'])
def get_choice():
    if session.get('is_admin'):
        return render_template("auth/choice.html")
    else:
        return redirect(url_for('get_index'))

@app.route('/admin', methods=["GET", "POST"])
def get_personas_admin():
    accion = request.args.get("accion")
    tipo = request.args.get("tipo", "personas")  # Usa 'personas' como valor por defecto
    personas = Persona.query.order_by(Persona.id.asc()).all()
    equipos = Equipo.query.order_by(Equipo.id.asc()).all()
    partidos = Partido.query.order_by(Partido.id.asc()).all()
    videos = Video.query.all()

    if not session.get('is_admin'):
        return redirect(url_for('get_index'))
    else:
        return render_template("admin/landing.html", accion = accion, tipo = tipo, personas = personas, equipos = equipos, partidos = partidos, videos = videos)

@app.route('/forms')
def get_forms():
    accion = request.args.get("accion", None)
    tipo = request.args.get("tipo", None)
    equipos = Equipo.query.all()
    personas = Persona.query.all()
    partidos = Partido.query.all()
    videos = Video.query.all()
    return render_template("components/forms.html", accion = accion, tipo = tipo, personas = personas, equipos = equipos, partidos = partidos, videos = videos)

# --- CRUD ---

# --- PERSONAS ---
# ------ AÑADIR PERSONA ------
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

    return render_template("components/forms.html", accion = "add", tipo = "personas")

# ------ LEER PERSONA ------
@app.route('/persona/<int:id>', methods=['GET', 'POST'])
def get_persona_by_id(id):
    persona = Persona.query.get(id)
    if not persona:
        return "Persona no encontrada", 404
    else:
        return render_template("players/datos_jugador.html", persona = persona)

# ------ EDITAR PERSONA ------
@app.route('/editar_persona/<int:id>', methods=['GET', 'POST'])
def editar_persona(id):
    persona = Persona.query.get(id)
    if not persona:
        return "Usuario no encontrado", 404
    if request.method == 'POST':
        persona.name = request.form.get('name')
        persona.surname = request.form.get('surname')
        persona.display_name = request.form.get('display_name')
        persona.number = int(request.form.get('number')) if request.form.get('number') else None
        persona.position = request.form.get('position')
        persona.dob = datetime.strptime(request.form.get('dob'), "%Y-%m-%d").date()
        persona.birthplace = request.form.get('birthplace')
        persona.nationality = request.form.get('nationality')
        persona.dominant_leg = request.form.get('dominant_leg')
        persona.is_international = request.form.get('is_international') == 'on'
        persona.is_trainer = request.form.get('is_trainer') == 'on'

        db.session.commit()
        return redirect(url_for('get_personas_admin'))
    
    return render_template("components/forms.html", accion = "edit", tipo = "personas", persona = persona)

# ------ BORRAR PERSONA ------
@app.route('/borrar_persona/<int:id>', methods=['GET', 'POST'])
def borrar_persona(id):
    persona = Persona.query.get(id)
    if not persona:
        return "Persona no encontrada", 404
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('get_personas_admin'))



# --- PARTIDOS ---
# ------ AÑADIR PARTIDO ------
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

    return render_template("components/forms.html", accion = "add", tipo = "partidos", equipos = Equipo.query.all())

# ------ EDITAR PARTIDO ------
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
    return render_template("components/forms.html", accion = "edit", tipo = "partidos", partido=partido, equipos=equipos)

# ------ BORRAR PARTIDO ------
@app.route('/borrar_partido/<int:id>', methods=['POST'])
def borrar_partido(id):
    partido = Partido.query.get(id)
    if not partido:
        return "Partido no encontrado", 404
    db.session.delete(partido)
    db.session.commit()
    return redirect(url_for('get_personas_admin', tipo='partidos'))



# --- EQUIPOS ---
# ------ AÑADIR EQUIPO ------
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

    return render_template("components/forms.html", accion = "add", tipo = "equipos")

# ------ EDITAR EQUIPO ------
@app.route('/editar_equipo/<int:id>', methods=['GET', 'POST'])
def editar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    if request.method == 'POST':
        equipo.name = request.form.get('name')
        equipo.abbreviation = request.form.get('abbreviation')
        db.session.commit()
        return redirect(url_for('get_personas_admin', tipo='equipos'))
    return render_template("components/forms.html", accion = "edit", tipo = "equipos", equipo = equipo)

# ------ BORRAR EQUIPO ------
@app.route('/borrar_equipo/<int:id>', methods=['POST'])
def borrar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    return redirect(url_for('get_personas_admin', tipo='equipos'))



# --- VIDEOS ---
# ------ AÑADIR VIDEO ------
@app.route('/add_video', methods=['GET', 'POST'])
def add_video():
    if request.method == 'POST':
        url = request.form.get('url')

        if '/' in url:
            identificador = url.split('/')[-1]
        else:
            return "URL inválida", 400

        new_video = Video(
            url=url,
            identificador=identificador
        )

        db.session.add(new_video)
        db.session.commit()
        return redirect(url_for('get_personas_admin'))

    return render_template("components/forms.html", accion = "add", tipo = "videos")


# --- EDITAR VIDEO ---
@app.route('/editar_video/<int:id>', methods=['GET', 'POST'])
def editar_video(id):
    video = Video.query.get(id)
    if not video:
        return "Vídeo no encontrado", 404

    if request.method == 'POST':
        video.url = request.form.get('url')
        db.session.commit()
        return redirect(url_for('get_personas_admin', tipo='videos'))

    return render_template("components/forms.html", accion = "edit", tipo = "videos", video = video)


# --- BORRAR VIDEO ---
@app.route('/borrar_video/<int:id>', methods=['POST'])
def borrar_video(id):
    video = Video.query.get(id)
    if not video:
        return "Vídeo no encontrado", 404
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('get_personas_admin', tipo='videos'))




# ----------- TIENDA ------------

# ÍNDEX
@app.route('/tenda', methods=['GET', 'POST'])
def mostrar_inicio():
    pagina = "store"

    productos = Producto.query.order_by(Producto.id.asc()).all()
    return render_template("tienda/index.html", pagina = pagina, productos = productos)

# REGISTRO USUARIO
@app.route('/register', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        mail = request.form.get('mail')
        password = request.form.get('password')

        if not mail or not password:
            return render_template("/auth/register.html", error="campos_vacios")
        
        user_exists = Usuario.query.filter_by(mail=mail).first()
        if user_exists:
            return render_template("/auth/register.html", error="usuario_existe")
        
        if len(password) < 8:
            return render_template("/auth/register.html", error="password_corto")
        
        new_user = Usuario(
            mail = mail,
            password = password,
            is_admin = False
        )
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('mostrar_inicio'))

    return render_template("/auth/register.html")

# ADMIN TIENDA
@app.route('/tenda/admin', methods=["GET", "POST"])
def get_productos_admin():
    productos = Producto.query.order_by(Producto.id.asc()).all()
    usuarios = Usuario.query.order_by(Usuario.id.asc()).all()

    if not session.get('is_admin'):
        return redirect(url_for('mostrar_inicio'))
    else:
        return render_template("admin/tienda.html", productos=productos, usuarios=usuarios)

# LEER TODOS LOS PRODUCTOS
@app.route('/tenda/productes', methods=['GET'])
def mostrar_productos():
    pagina = "store"

    productos = Producto.query.order_by(Producto.id.asc()).all()
    return render_template("tienda/productes.html", pagina = pagina, productos = productos)

# LEER PRODUCTO ESPECÍFICO
@app.route('/tenda/producte/<int:id>', methods=['GET', 'POST'])
def mostrar_producto(id):
    pagina = "store"

    producto = Producto.query.get(id)
    if not producto:
        return "producto no encontrado", 404
    return render_template("tienda/producte.html", pagina = pagina, producto = producto)

# CREAR PRODUCTO
@app.route('/tenda/add_producto', methods=['GET', 'POST'])
def add_producto():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        collection = request.form.get('collection')
        price = request.form.get('price')
        
        
        new_producto = Producto(
            name=name,
            desc=desc,
            collection=collection,
            price=price
        )
        
        db.session.add(new_producto)
        db.session.commit()
        return redirect(url_for('mostrar_inicio'))

    return render_template("components/forms.html", accion = "add", tipo = "productos")

# EDITAR PRODUCTO
@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return "Producto no encontrado.", 404
    if request.method == 'POST':
        producto.name = request.form.get('name')
        producto.desc = request.form.get('desc')
        producto.price = request.form.get('price')
        db.session.commit()
        return redirect(url_for('get_productos_admin'))
    
    return render_template("components/forms.html", accion = "edit", tipo = "productos", producto = producto)

# BORRAR PRODUCTO
@app.route('/tenda/borrar_producto/<int:id>', methods=['GET', 'POST'])
def borrar_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return "Producto no encontrado.", 404
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('get_productos_admin'))

# ADD A CARRITO
@app.route('/add_al_carrito/<int:producto_id>', methods=['GET', 'POST'])
def add_al_carrito(producto_id):
    if session.get('user_login'):
        producto = Producto.query.get(producto_id)
        
        if producto:
            producto.in_cart = True
            db.session.commit()
    
        return redirect(url_for('mostrar_inicio'))
    
    else:
        return redirect(url_for('get_login'))

# VISUALIZAR CARRITO
@app.route('/tenda/carrito', methods=['GET', 'POST'])
def ver_carrito():
    pagina = "store"

    if not session.get('user_login'):
        return redirect(url_for('mostrar_inicio'))

    productos_en_carrito = Producto.query.filter_by(in_cart=True).all()
    
    precio_total = None
    descuento_aplicado = 0
    codigo_descuento = None

    if request.method == 'POST':
        if 'actualizar' in request.form:
            producto_id = int(request.form['actualizar'])
            qty_str = request.form.get(f'qty_{producto_id}')
            
            if qty_str is None or not qty_str.isdigit():
                return "Cantidad no válida", 400 

            qty = int(qty_str)
            producto = Producto.query.get(producto_id)
            if producto:
                producto.qty = qty
                db.session.commit()

        elif 'eliminar' in request.form:
            producto_id = int(request.form['eliminar'])
            
            producto = Producto.query.get(producto_id)
            if producto:
                producto.in_cart = False
                db.session.commit()

        elif 'checkout' in request.form:
            total = 0
            for producto in productos_en_carrito:
                if producto.qty is None: 
                    producto.qty = 1
                total += producto.price * producto.qty
            precio_total = total

        elif 'aplicar_descuento' in request.form:
            codigo_descuento = request.form.get('codigo_descuento')
            promo = Promo.query.filter_by(tag=codigo_descuento).first()
            
            if promo:
                descuento_aplicado = promo.discount
                total = 0
                for producto in productos_en_carrito:
                    if producto.qty is None: 
                        producto.qty = 1
                    total += producto.price * producto.qty
                precio_total = total - (total * descuento_aplicado / 100)
                precio_total = round(precio_total, 2)
            else:
                precio_total = None

        return render_template("tienda/carrito.html", pagina = pagina, productos_en_carrito = productos_en_carrito, precio_total = precio_total, descuento_aplicado = descuento_aplicado, codigo_descuento = codigo_descuento)

    return render_template("tienda/carrito.html", pagina = pagina, productos_en_carrito = productos_en_carrito)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('mostrar_inicio'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)