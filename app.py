import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

# --- App Configuration ---
app = Flask(__name__)
DATABASE = 'licenses.db'


# --- Database Functions ---
def get_db():
    """Connect to the application's configured database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Allows accessing columns by name
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database from the schema file."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("Initialized the database.")


# --- Web Application Routes ---
@app.route('/')
def index():
    """Main page, displays licenses and handles searching."""
    db = get_db()
    search_query = request.args.get('search', '').strip()

    if search_query:
        # If there's a search term, filter results by name or company
        cursor = db.execute(
            'SELECT * FROM licenses WHERE name LIKE ? OR company LIKE ? '
            'ORDER BY name ASC',
            ['%' + search_query + '%', '%' + search_query + '%']
        )
    else:
        # Otherwise, get all licenses
        cursor = db.execute('SELECT * FROM licenses ORDER BY name ASC')

    licenses = cursor.fetchall()
    # Pass search query back to template to keep it in the search box
    return render_template(
        'index.html', licenses=licenses, search_query=search_query
    )


@app.route('/add_license', methods=['POST'])
def add_license():
    """Handles adding a new license to the database."""
    db = get_db()

    # Handle optional date fields, ensuring empty strings become NULL
    start_date = request.form.get('start_date') or None
    end_date = request.form.get('end_date') or None

    db.execute(
        'INSERT INTO licenses (name, category, company, assigned_to, '
        'license_type, serial_number, start_date, end_date) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        [
            request.form['name'], request.form['category'],
            request.form['company'], request.form['assigned_to'],
            request.form['license_type'], request.form['serial_number'],
            start_date, end_date
        ]
    )
    db.commit()
    return redirect(url_for('index'))


# --- Main execution ---
if __name__ == '__main__':
    # Initialize the database if the file doesn't exist
    try:
        # A simple check; in a real app, use a migration tool like Alembic
        with open(DATABASE, 'r'):
            pass
    except FileNotFoundError:
        print("Database not found, initializing...")
        init_db()

    app.run(debug=True, host='0.0.0.0')