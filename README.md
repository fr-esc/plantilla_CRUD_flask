# plantilla_CRUD_flask

Plantilla de arranque para construir un CRUD (Crear, Leer, Actualizar, Borrar) con **Flask** y **Bootstrap 4**.

La idea es que no empieces desde cero: esta plantilla ya tiene la estructura de un CRUD completo funcionando con **datos en memoria**. Cuando la necesites, la adaptas a tu caso concreto (base de datos, más campos, más tablas, etc.).

---

## Qué hace esta plantilla

Es un pequeño CRUD de "transacciones" bancarias (fecha y monto) que sirve como ejemplo didáctico de las 4 operaciones:

| Operación | Ruta               | Método | Qué hace                              |
|-----------|--------------------|--------|---------------------------------------|
| **C**rear | `/add`             | GET/POST | Muestra el formulario y guarda una nueva transacción |
| **R**ead  | `/`                | GET    | Lista todas las transacciones         |
| **U**pdate| `/edit/<id>`       | GET/POST | Muestra el formulario y modifica una transacción |
| **D**elete| `/delete/<id>`     | GET    | Elimina una transacción               |

---

## Estructura de archivos

```
flask_plantilla_CRUD/
├── app.py                  # Toda la lógica de la aplicación (rutas del CRUD)
├── README.md               # Este documento
├── requirements.txt        # Dependencias del proyecto
├── .gitignore              # Archivos que no se suben a git
└── templates/
    ├── transactions.html   # Lista de registros (vista principal)
    ├── form.html           # Formulario para CREAR
    ├── edit.html           # Formulario para EDITAR
    └── search.html         # Formulario de búsqueda (sin ruta, ver notas)
```

---

## Requisitos

- **Python 3** (recomendado 3.10 o superior)
- **pip**

---

## Instalación y puesta en marcha

1. **Crear y activar un entorno virtual** (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux / macOS
   venv\Scripts\activate           # Windows
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**

   ```bash
   python app.py
   ```

4. **Abrir el navegador** en: <http://127.0.0.1:5000>

---

## Cómo funciona el código (resumen)

Todo está en `app.py`. El punto clave es la lista `transactions`, que actúa como la "base de datos" de ejemplo:

```python
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    ...
]
```

Cada **ruta** de Flask hace una de las 4 operaciones del CRUD:

- `get_transactions()` → **R**: pinta la tabla con todas las transacciones.
- `add_transaction()` → **C**: si llega un POST guarda el nuevo registro; si llega un GET muestra el formulario.
- `edit_transaction(<id>)` → **U**: si llega un POST actualiza el registro; si llega un GET muestra el formulario precargado.
- `delete_transaction(<id>)` → **D**: busca el registro por su ID y lo elimina.

El patrón **GET = mostrar formulario / POST = guardar** es el estándar en Flask y lo verás en `add` y `edit`.

---

## Cómo adaptarla a tu proyecto (guía rápida)

Esta sección te dice qué tocar según lo que necesites.

### 1. Cambiar los campos del registro

1. Cambia la lista de ejemplo en `app.py`.
2. Ajusta las líneas de `request.form['...']` en las rutas `add` y `edit`.
3. Actualiza las tablas y formularios en `templates/transactions.html`, `form.html` y `edit.html`.

### 2. Conectar una base de datos real (SQLite)

El paso más habitual. Cuando necesites persistir datos entre reinicios:

- Instala **Flask-SQLAlchemy**: `pip install flask-sqlalchemy`
- Crea una clase `Modelo(db.Model)` que represente tu tabla.
- Reemplaza las operaciones sobre `transactions` (append, for, remove) por consultas del ORM:
  - Crear → `db.session.add(nuevo)` + `db.session.commit()`
  - Leer → `Modelo.query.all()`
  - Editar → buscar con `Modelo.query.get(id)` y modificar atributos
  - Borrar → `db.session.delete(objeto)` + `db.session.commit()`

### 3. Añadir una tabla nueva (segundo modelo)

Duplica el patrón completo: crea la lista/DB, agrega 4 rutas nuevas (listar, crear, editar, borrar) y crea 2–3 plantillas nuevas siguiendo las existentes.

### 4. Activar la búsqueda

El template `templates/search.html` ya está creado pero **no tiene ruta en `app.py`** (quedó sin terminar). Para usarlo:

1. Agrega una ruta, por ejemplo `/search`, que renderice `search.html`.
2. En la función, lee `min_amount` y `max_amount` del formulario y filtra la lista:

   ```python
   @app.route("/search", methods=["GET", "POST"])
   def search_transactions():
       if request.method == 'POST':
           min_amount = float(request.form['min_amount'])
           max_amount = float(request.form['max_amount'])
           results = [t for t in transactions if min_amount <= t['amount'] <= max_amount]
           return render_template("transactions.html", transactions=results)
       return render_template("search.html")
   ```

3. Enlaza el botón "Search" desde `transactions.html`.

---

## Limitaciones conocidas (por diseño)

Estas no son fallas, sino características de la plantilla que debes tener presentes:

- **Los datos se pierden al reiniciar** el servidor (lista en memoria, no hay BD).
- **Los IDs se calculan con `len(transactions) + 1`**; si borras un registro, puede haber IDs duplicados. Con una base de datos esto se resuelve solo.
- **No hay mensajes de error** en la interfaz si un registro no se encuentra (el borrado redirige silenciosamente).
- **`debug=True` está activo** para desarrollo. Nunca lo dejes así en producción.
- **El CSS se repite** en las 4 plantillas; si cambias el diseño, recuerda cambiarlo en todas (o muévelo a un archivo `static/`).

---

## Próximos pasos sugeridos

1. Conectar SQLite (la mejora más útil).
2. Agregar `templates/base.html` para no repetir el HTML en cada plantilla.
3. Mover el CSS a `static/css/estilo.css`.
4. Añadir mensajes `flash()` para avisar de errores/éxitos.
5. Completar la ruta de búsqueda que quedó sin terminar.
