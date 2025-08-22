import os
import pyodbc
from flask import Flask, render_template, request, redirect, url_for, g, flash

# --- App Configuration ---
app = Flask(__name__)
app.secret_key = 'your_asset_management_secret_key'

# --- MS SQL Server Configuration (reads from environment variables) ---
MSSQL_SERVER = os.environ.get('MSSQL_SERVER')
MSSQL_DATABASE = os.environ.get('MSSQL_DATABASE')
MSSQL_USERNAME = os.environ.get('MSSQL_USERNAME')
MSSQL_PASSWORD = os.environ.get('MSSQL_PASSWORD')
MSSQL_DRIVER = '{ODBC Driver 18 for SQL Server}'


def get_db():
    """Establish and return a database connection."""
    if 'db' not in g:
        if not all([MSSQL_SERVER, MSSQL_DATABASE, MSSQL_USERNAME, MSSQL_PASSWORD]):
            raise ValueError("Database credentials are not fully configured.")

        conn_str = (
            f'DRIVER={MSSQL_DRIVER};'
            f'SERVER=tcp:{MSSQL_SERVER},1433;'
            f'DATABASE={MSSQL_DATABASE};'
            f'UID={MSSQL_USERNAME};'
            f'PWD={MSSQL_PASSWORD};'
        )