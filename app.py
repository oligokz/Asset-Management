import os
import pyodbc
from flask import Flask, render_template, request, redirect, url_for, g, flash

# --- App Configuration ---
app = Flask(__name__)
app.secret_key = 'your_asset_management_secret_key'

# --- MS SQL Server Configuration (reads from environment variables/secrets) ---
def read_secret_or_env(var_name):
    """Reads a variable from a file path specified by an env var, or the env var itself."""
    file_path = os.environ.get(f'{var_name}_FILE')
    if file_path:
        try:
            with open(file_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
    return os.environ.get(var_name)

MSSQL_SERVER = read_secret_or_env('MSSQL_SERVER')
MSSQL_DATABASE = read_secret_or_env('MSSQL_DATABASE')
MSSQL_USERNAME = read_secret_or_env('MSSQL_USERNAME')
MSSQL_PASSWORD = read_secret_or_env('MSSQL_PASSWORD')
MSSQL_DRIVER = '{ODBC Driver 17 for SQL Server}'

def get_db():
    """Connect to the MS SQL Server database."""
    if 'db' not in g:
        conn_str = (
            f'DRIVER={MSSQL_DRIVER};'
            f'SERVER=tcp:{MSSQL_SERVER},1433;'
            f'DATABASE={MSSQL_DATABASE};'
            f'UID={MSSQL_USERNAME};'
            f'PWD={MSSQL_PASSWORD};'
        )
        g.db = pyodbc.connect(conn_str)
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Routes ---
@app.route('/')
def index():
    """Main dashboard to view all assets."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM assets ORDER BY name ASC')
    assets = cursor.fetchall()
    return render_template('index.html', assets=assets)

@app.route('/add', methods=['GET', 'POST'])
def add_asset():
    """Page to add a new asset."""
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor()
        sql = """
        INSERT INTO assets (asset_tag, name, category, status, location, purchase_date, purchase_cost, serial_number, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            request.form['asset_tag'], request.form['name'],
            request.form['category'], request.form['status'],
            request.form['location'], request.form['purchase_date'] or None,
            request.form['purchase_cost'] or None, request.form['serial_number'],
            request.form['notes']
        )
        cursor.execute(sql, params)
        conn.commit()
        flash('Asset added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_asset.html')

# (Routes for edit, view details, and history will be added in the next phase)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')