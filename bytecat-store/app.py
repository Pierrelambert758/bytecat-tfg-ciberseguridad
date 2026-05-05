import sqlite3
from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "bytecat_secret_key"


def get_db_connection():
    connection = sqlite3.connect("bytecat.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def inicio():
    connection = get_db_connection()

    products = connection.execute("""
        SELECT * FROM products
        WHERE name IN (
            'Lenovo ThinkPad X1',
            'Teclado mecánico RGB',
            'Router TP-Link AX50',
            'Cámara IP 1080p',
            'Monitor Dell 24"',
            'SSD Kingston 1TB'
        )
        LIMIT 6
    """).fetchall()

    connection.close()

    return render_template("index.html", products=products)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()
        query = f"SELECT * FROM web_users WHERE username = '{username}' AND password = '{password}' AND active = 1"
        user = connection.execute(query).fetchone()
        connection.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect("/")
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    users = connection.execute("SELECT username, role, email FROM web_users").fetchall()
    notes = connection.execute("SELECT title, content FROM admin_notes").fetchall()

    connection.close()

    return render_template("admin.html", users=users, notes=notes)

@app.route("/empresa")
def empresa():
    return render_template("empresa.html")


@app.route("/empresa-interna")
def empresa_interna():
    return render_template("empresa2.html")

@app.route("/informacion")
def informacion():
    return render_template("informacion.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    comentario = None

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        mensaje = request.form["mensaje"]

        comentario = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "mensaje": mensaje
        }

    return render_template("contacto.html", comentario=comentario)

@app.route("/catalogo")
def catalogo():
    connection = get_db_connection()
    products = connection.execute("SELECT * FROM products").fetchall()
    connection.close()

    return render_template("catalogo.html", products=products)

@app.route("/admin/catalogo", methods=["GET", "POST"])
def admin_catalogo():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_db_connection()

    if request.method == "POST":
        product_id = request.form["product_id"]
        new_price = request.form["price"]

        connection.execute(
            "UPDATE products SET price = ? WHERE id = ?",
            (new_price, product_id)
        )

        connection.commit()
        flash("Precio actualizado correctamente.", "success")

    products = connection.execute("SELECT * FROM products").fetchall()
    connection.close()

    return render_template("admin_catalogo.html", products=products)

@app.route("/carrito")
def carrito():
    return render_template("carrito.html")

@app.route("/admin/pedidos")
def admin_pedidos():
    connection = sqlite3.connect("bytecat.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT orders.id,
           customers.first_name,
           customers.last_name,
           customers.email,
           orders.total_price,
           orders.payment_method,
           orders.order_status,
           orders.created_at
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
    """)

    pedidos = cursor.fetchall()
    connection.close()

    return render_template("admin_pedidos.html", pedidos=pedidos)

@app.route("/admin/clientes")
def admin_clientes():
    connection = sqlite3.connect("bytecat.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customers")
    clientes = cursor.fetchall()

    connection.close()

    return render_template("admin_clientes.html", clientes=clientes)

if __name__ == "__main__":
    app.run(debug=True)
