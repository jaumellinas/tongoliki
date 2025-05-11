![Mockup](static/img/mockup.png)

# Proyecto página RCD Mallorca

## Integrantes
- Irene Fontcuberta León
- Jaume Llinàs Sansó
- Daniel Cobo Palao
- Adrià Garí Sagrera

---

## 📝 Explicación del proyecto

Este proyecto consiste en una página web dedicada al club de fútbol **RCD Mallorca**. Ha sido desarrollada utilizando el framework **Flask**, trabajando con tecnologías como **Python**, **HTML** y **CSS**.

El objetivo es mostrar una web informativa y funcional sobre el club, con apartados dinámicos como vídeos, plantilla de jugadores, y un backoffice de administración (zona privada) para modificar o eliminar el contenido.

- Los archivos relacionados con el **frontend** se encuentran en el directorio `/templates` y los estilos en la carpeta `/static`.
- Toda la lógica está centralizada en el archivo `app.py`.

---

## 👥 Organización del equipo

El grupo se ha organizado en dos departamentos para dividir responsabilidades:

### 🎨 Frontend
- **Integrantes**: Jaume e Irene  
- **Responsabilidades**:
  - Diseño visual del sitio web.
  - Creación y maquetación de páginas HTML.
  - Desarrollo de estilos con CSS para lograr una estética coherente y adaptada al tema del RCD Mallorca.
  - Estructuración del contenido para una buena experiencia de usuario.

### ⚙️ Backend
- **Integrantes**: Dani y Adri  
- **Responsabilidades**:
  - Implementación de la lógica de la aplicación con Flask.
  - Gestión de rutas y sesiones.
  - Conexión con la base de datos Supabase.
  - Buenas prácticas de programación y legibilidad del código.

---

## 🚀 Ejecución del proyecto

### 1. Instalación de dependencias
Antes de ejecutar el proyecto, asegúrate de tener un entorno virtual y de instalar las dependencias necesarias con:

```bash
pip install -r requirements.txt
```

### 2. Ejecución
Puedes iniciar el servidor con:

```bash
flask run
```
O bien, desde Visual Studio Code, seleccionando el archivo app.py y haciendo clic en el botón de Play (▶️).
Asegúrate de tener configurada la variable de entorno FLASK_APP=app.py si ejecutas manualmente.

### 3. Configuración del archivo '.env'
Es necesario crear un archivo llamado '.env' en la raíz del proyecto. Este archivo debe contener la URL de conexión a la base de datos de Supabase. En nuestro caso, dicho secreto de entorno se encuentra ya creado **en la versión entregable del proyecto**.

---

## 🛢️ Base de datos

La base de datos utilizada está alojada en la nube, utilizando el servicio Supabase, que permite gestionar tablas, autenticación y almacenamiento de datos.

---

## 📋 Diagramas UML

Hemos creado unos diagramas UML, concretamente de clases y de estado, para facilitar la documentación del proyecto.


Diagrama de Clases

![Diagrama de Clases](static/img/UML/diagrama_clases.jpg)


Diagrama de Estado de esas clases

![Diagrama de Estado](static/img/UML/entidades_diagrama_estado.jpg)


Diagrama de Estado del login (backoffice)

![Diagrama de Estado del Login](static/img/UML/login_diagrama_estado.jpg)

---

## 🔐 Acceso al backoffice (modo prueba)

Para acceder al panel de administración (zona privada), puedes usar las siguientes credenciales de prueba:

- **Correo**: tongoliki@gmail.com

- **Contraseña**: 12345  
<br><br>
# 🛍️ Tienda del proyecto RCD Mallorca! ⚽

Esta sección del proyecto es un subproyecto donde hacemos nuestra **réplica** de la **tienda del RCD Mallorca**. En este apartado, contamos con una modificación en los integrantes, puesto que uno de ellos no participa en él.

## Integrantes:
- Adrià Garí Sagrera
- Jaume Llinàs Sansó
- Irene Fontcuberta León

## Explicación del subproyecto

En esta ocasión, estamos recreando la tienda del RCD Mallorca, donde continuamos utilizando lo mismo que en el proyecto principal: Flask como framework principal, Python, HTML y CSS. 

Todos lo relacionado al **frontend** de esta tienda se encontrará dentro de la ruta `/templates/tienda` y sus estilos en `/static/styles` usando el archivo CSS principal. En el caso del **backend** todo se encuentra en el propio archivo `app.py` junto con el proyecto principal.


## Funciones de los equipos

Como en el caso anterior, hemos dividido el equipo en dos departamentos:

### 🎨 Frontend:
- **Integrantes**: Jaume Llinàs e Irene Fontcuberta
- **Responsabilidades**:
  - Diseño visual de la tienda, carrito y páginas login/register
  - Maquetaciones y 'mockups'
  - Cuidar la experiencia de usuario
  - Cuidar la imagen de marca

### ⚙️ Backend: 
- **Integrantes**: Adrià Garí
- **Responsabilidades**:
  - Creación de las clases, objetos y modelos
  - Métodos y funciones de la página web
  - Implementación de lógica
  - Funciones Login/Register
  - Implementar un carrito


## Diagramas UML

También hemos creado unos diagramas UML para nuestra tienda!

### Diagrama de Clases

![Diagrama de Clases](static/img/tenda/UML/clases.jpg)

---

### Diagramas de Estado

Producto

![Producto](static/img/tenda/UML/producto.jpg)
---

Carrito

![Carrito](static/img/tenda/UML/carrito.jpg)
---

Login

![Login](static/img/tenda/UML/login.jpg)
---

Registro

![Registro](static/img/tenda/UML/registro.jpg)
---