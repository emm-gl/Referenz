from flask import Flask, render_template, request, redirect, url_for,session,jsonify, flash
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "asdasdsa"

BACKENDLESS_URL = 'https://api.backendless.com/69DA66B9-D1A8-C396-FF6B-10897D65A600/DBA10B8A-452F-4D8D-AE29-C1A70D9B2CA5/data/'

# Puedes obtener el APP_ID y REST_API_KEY al registrarte en Backendless.

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        # Manejar la creación del cliente en Backendless
        if obtener_cliente(request.form['id']) is None:
            cliente_data = {
                'id': request.form['id'],
                'nombre': request.form['nombre'],
                'direccion': request.form['direccion']
            }
            create_cliente(cliente_data)
        session['id_cliente'] = request.form['id']
        return redirect(url_for('productos'))

    return render_template('clientes.html')

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    # Obtener la lista de productos desde Backendless
    productos = get_productos()

    if request.method == 'POST':
        # Manejar la selección de productos y creación de la orden en Backendless
        productos_seleccionados = request.form.getlist('productos')


        return create_orden(productos_seleccionados,session['id_cliente'] )

    return render_template('productos.html', productos=productos)

#################################################################
# Protegida. Solo pueden entrar los que han iniciado sesión
@app.route("/escritorio")
def escritorio():
    return render_template("escritorio.html")

# Formulario para iniciar sesión
@app.route("/login")
def login():
    return render_template("login.html")

# Manejar login
@app.route("/hacer_login", methods=["POST"])
def hacer_login():
    correo = request.form["correo"]
    palabra_secreta = request.form["palabra_secreta"]
    # Aquí comparamos. 
    if correo == "Tienda_001@gmail.com" and palabra_secreta == "Abc123$":       #####<--------------------- User and Password
        # Si coincide, iniciamos sesión y además redireccionamos
        session["usuario"] = correo

        return redirect("/escritorio")
    else:
        # Si NO coincide, lo regresamos
        flash("Correo o contraseña incorrectos")
        return redirect("/login")

# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

"""
# Un "middleware" que se ejecuta antes de responder a cualquier ruta. Aquí verificamos si el usuario ha iniciado sesión
@app.before_request
def antes_de_cada_peticion():
    ruta = request.path
    # Si no ha iniciado sesión y no quiere ir a algo relacionado al login, lo redireccionamos al login
    if not 'usuario' in session and ruta != "/login" and ruta != "/hacer_login" and ruta != "/logout" and not ruta.startswith("/static"):
        flash("Inicia sesión para continuar")
        return redirect("/login")
    # Si ya ha iniciado, no hacemos nada, es decir lo dejamos pasar
"""






def obtener_cliente(user_id):
    response = requests.get(BACKENDLESS_URL + f"Clientes?where=IdCliente%3D{user_id}")
    return response.json() if response.status_code == 200 else None


def create_cliente(data):
    response = requests.post(BACKENDLESS_URL + 'Clientes', json=data)
    return response.json()

def get_productos():
    response = requests.get(BACKENDLESS_URL + 'Productos')
    return response.json()

def create_orden(productos, id_cliente):
    order_data = []
    for i in productos:
        order = {
                    'IdOrden': 1001,
                    'FechaOrden': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'IdCliente': int(id_cliente),
                    'IdProducto': int(i),
                    'Fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Cantidad': 1,
                    '___class': 'Ordenes'
                }
        response = requests.post(BACKENDLESS_URL + 'Ordenes', json=order)

def get_orders():
    response = requests.get(BACKENDLESS_URL + 'Ordenes')
    return response.json()



# Send POST request to insert new orders
    
    print(response.content)
    # Check if request was successful
    if response.status_code == 200:
        return 'Orden creada con éxito'
    else:
        return 'Error al crear la orden'
    

if __name__ == '__main__':
    app.run(debug=True)
