import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, flash

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_change_this'
DATABASE = 'licenses.db'

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
        print("Initialized the database.")

@app.route('/')
def index():
    db = get_db()
    search_query = request.args.get('search', '').strip()

    presets_cursor = db.execute('SELECT preset_type, value FROM presets ORDER BY value ASC')
    presets_data = presets_cursor.fetchall()
    presets = {
        'software': [p['value'] for p in presets_data if p['preset_type'] == 'software'],
        'company': [p['value'] for p in presets_data if p['preset_type'] == 'company']
    }

    if search_query:
        cursor = db.execute(
            'SELECT * FROM licenses WHERE name LIKE ? OR company LIKE ? ORDER BY name ASC',
            ['%' + search_query + '%', '%' + search_query + '%']
        )
    else:
        cursor = db.execute('SELECT * FROM licenses ORDER BY name ASC')

    licenses = cursor.fetchall()
    return render_template('index.html', licenses=licenses, presets=presets, search_query=search_query)

@app.route('/add_license', methods=['POST'])
def add_license():
    db = get_db()
    start_date = request.form.get('start_date') or None
    end_date = request.form.get('end_date') or None
    db.execute(
        'INSERT INTO licenses (name, company, assigned_to, license_type, serial_number, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [
            request.form['name'], request.form['company'],
            request.form['assigned_to'], request.form['license_type'],
            request.form['serial_number'], start_date, end_date
        ]
    )
    db.commit()
    flash('License added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<int:license_id>')
def edit_license(license_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM licenses WHERE id = ?', [license_id])
    license_data = cursor.fetchone()
    if license_data is None:
        flash('License not found!', 'error')
        return redirect(url_for('index'))
    return render_template('edit_license.html', license=license_data)

@app.route('/update/<int:license_id>', methods=['POST'])
def update_license(license_id):
    db = get_db()
    start_date = request.form.get('start_date') or None
    end_date = request.form.get('end_date') or None
    db.execute(
        'UPDATE licenses SET name=?, company=?, assigned_to=?, license_type=?, serial_number=?, start_date=?, end_date=? WHERE id = ?',
        [
            request.form['name'], request.form['company'],
            request.form['assigned_to'], request.form['license_type'],
            request.form['serial_number'], start_date, end_date, license_id
        ]
    )
    db.commit()
    flash('License updated successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/presets', methods=['GET', 'POST'])
def manage_presets():
    db = get_db()
    if request.method == 'POST':
        preset_type = request.form['preset_type']
        value = request.form['value'].strip()
        if preset_type and value:
            try:
                db.execute('INSERT INTO presets (preset_type, value) VALUES (?, ?)', [preset_type, value])
                db.commit()
                flash(f'Preset "{value}" added successfully!', 'success')
            except sqlite3.IntegrityError:
                flash(f'Preset "{value}" already exists.', 'error')
        return redirect(url_for('manage_presets'))

    presets_cursor = db.execute('SELECT id, preset_type, value FROM presets ORDER BY preset_type, value ASC')
    all_presets = presets_cursor.fetchall()
    return render_template('presets.html', presets=all_presets)

@app.route('/presets/delete/<int:preset_id>', methods=['POST'])
def delete_preset(preset_id):
    db = get_db()
    db.execute('DELETE FROM presets WHERE id = ?', [preset_id])
    db.commit()
    flash('Preset deleted successfully!', 'success')
    return redirect(url_for('manage_presets'))

if __name__ == '__main__':
    try:
        with open(DATABASE, 'r'): pass
    except FileNotFoundError:
        print("Database not found, initializing...")
        init_db()
    app.run(debug=True, host='0.0.0.0')