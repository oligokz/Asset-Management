import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = 'licenses.db'

# --- Database Functions ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# --- Web Application Routes ---
@app.route('/')
def index():
    """Main page, displays all licenses."""
    db = get_db()
    cursor = db.execute('SELECT * FROM licenses ORDER BY name ASC')
    licenses = cursor.fetchall()
    return render_template('index.html', licenses=licenses)

@app.route('/add_license', methods=['POST'])
def add_license():
    """Handles adding a new license."""
    name = request.form['name']
    category = request.form['category']
    company = request.form['company']
    assigned_to = request.form['assigned_to']
    license_type = request.form['license_type']
    serial_number = request.form['serial_number'] # Get the new field

    db = get_db()
    # Updated SQL to include the new field
    db.execute(
        'INSERT INTO licenses (name, category, company, assigned_to, license_type, serial_number) VALUES (?, ?, ?, ?, ?, ?)',
        [name, category, company, assigned_to, license_type, serial_number]
    )
    db.commit()
    return redirect(url_for('index'))

# --- Main execution ---
if __name__ == '__main__':
    # Initialize the database if the file doesn't exist
    try:
        with open(DATABASE): pass
    except IOError:
        print("Database not found, initializing...")
        init_db()
        
    app.run(debug=True, host='0.0.0.0')