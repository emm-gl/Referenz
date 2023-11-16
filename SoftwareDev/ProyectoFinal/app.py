from flask import Flask, render_template, request, redirect, url_for,session,jsonify, flash
from datetime import datetime
import requests
import os
import pandas as pd
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


# Página Protegida. Solo pueden entrar los que han iniciado sesión, en este caso el tendero
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

#Descargar CSV
@app.route("/GetCSV/", methods=['POST'])
def getCSV():
    forward_message = "getting CSV..."
    print(forward_message)

    fecha_actual = datetime.now().date()
    fecha_corta = fecha_actual.strftime('%Y-%m-%d')

    CSV_path = os.path.join(os.path.expanduser("~"), "Downloads") + '\Orders_' + fecha_corta +'.csv'
    response = requests.get(BACKENDLESS_URL + 'Ordenes')
    df_ordenes = pd.DataFrame(response.json())
    df_ordenes.to_csv(CSV_path, index = False)
    return redirect("/login")


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



# Send POST request to insert new orders
    
    print(response.content)
    # Check if request was successful
    if response.status_code == 200:
        return 'Orden creada con éxito'
    else:
        return 'Error al crear la orden'
    

if __name__ == '__main__':
    app.run(debug=True)
