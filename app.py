# ============================================================
# plantilla_CRUD_flask
# Plantilla de CRUD en Flask con datos en memoria.
# Cuando la adaptes: cambia la lista "transactions" por tu base
# de datos o modelo, y ajusta los campos de los formularios.
# ============================================================

# Importar los componentes de Flask que vamos a usar
# - Flask: crea la aplicación web
# - redirect: envía al navegador a otra ruta
# - request: accede a los datos enviados por los formularios
# - render_template: pinta los archivos HTML de la carpeta templates/
# - url_for: genera URLs a partir del nombre de la función de una ruta
from flask import Flask, redirect, request, render_template, url_for

# Crear la instancia de la aplicación Flask
app = Flask(__name__)


# ============================================================
# "Base de datos" de ejemplo (en memoria)
# ============================================================
# Esta lista hace de tabla de datos. Se pierde al reiniciar el servidor.
# Para un CRUD real, reemplázala por una base de datos (SQLite, etc.).
# Formato de cada registro: {'id': int, 'date': str, 'amount': float}
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# ------------------------------------------------------------
# OPERACIÓN READ (Leer) — listar todos los registros
# ------------------------------------------------------------
# Ruta principal "/". Pinta la tabla de transacciones.
# render_template pasa la lista "transactions" a la plantilla
# para que la recorra con un bucle Jinja2.
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# ------------------------------------------------------------
# OPERACIÓN CREATE (Crear) — agregar un nuevo registro
# ------------------------------------------------------------
# Una misma ruta con dos comportamientos según el método:
#   GET  -> muestra el formulario vacío (form.html)
#   POST -> guarda los datos enviados por el formulario
# Este patrón GET/POST es el estándar en Flask.
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Si llega un POST significa que el formulario fue enviado
    if request.method == 'POST':
        # Crear un nuevo diccionario con los datos del formulario.
        # request.form['campo'] lee cada campo por su atributo "name".
        # OJO: el ID usa len()+1, no es fiable si borras registros;
        # con una base de datos se resuelve automáticamente.
        transaction = {
            'id': len(transactions) + 1,            # Nuevo ID (ver nota arriba)
            'date': request.form['date'],           # Campo "date" del formulario
            'amount': float(request.form['amount']) # Campo "amount", convertido a número decimal
        }
        # Añadir el nuevo registro a la lista (aquí iría db.session.add)
        transactions.append(transaction)

        # Redirigir a la lista para que el usuario vea el cambio
        return redirect(url_for("get_transactions"))
    
    # Si llega un GET, solo mostramos el formulario de creación
    return render_template("form.html")

# ------------------------------------------------------------
# OPERACIÓN UPDATE (Actualizar) — modificar un registro
# ------------------------------------------------------------
# <int:transaction_id> captura el ID desde la URL (ej: /edit/2).
# Mismo patrón GET/POST que en "add".
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Valores nuevos enviados por el formulario de edición
        date = request.form['date']           # Campo "date"
        amount = float(request.form['amount'])# Campo "amount", convertido a float

        # Buscar el registro que coincida con el ID de la URL y actualizarlo.
        # Aquí en vez del bucle iría una consulta a la base de datos.
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Sobrescribir la fecha
                transaction['amount'] = amount   # Sobrescribir el monto
                break                            # Salir del bucle al encontrarlo

        # Redirigir a la lista tras actualizar
        return redirect(url_for("get_transactions"))
    
    # Si es GET, buscar el registro para precargar el formulario de edición
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Pasar el registro encontrado a edit.html (rellena el formulario)
            return render_template("edit.html", transaction=transaction)

    # Si el ID no existe, devolver un error 404 en formato JSON.
    # Idealmente se mostraría una página de error amigable.
    return {"message": "Transaction not found"}, 404


# ------------------------------------------------------------
# OPERACIÓN DELETE (Borrar) — eliminar un registro
# ------------------------------------------------------------
# Ruta que se invoca desde el botón "Delete" de la tabla.
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Buscar el registro por ID y quitarlo de la lista.
    # Con base de datos sería: db.session.delete(objeto) + commit.
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Eliminar el registro de la lista
            break  # Salir del bucle

    # Redirigir a la lista tras eliminar.
    # OJO: no avisa al usuario si el ID no existía.
    return redirect(url_for("get_transactions"))

# ------------------------------------------------------------
# Punto de entrada de la aplicación
# ------------------------------------------------------------
# Solo se ejecuta cuando corremos "python app.py" directamente
# (no cuando se importa desde otro archivo).
# debug=True: recarga el servidor al guardar y muestra errores.
# DESACTÍVALO en producción.
if __name__ == "__main__":
    app.run(debug=True)
    