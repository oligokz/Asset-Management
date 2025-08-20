CREATE TABLE licenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  category TEXT,
  company TEXT,
  assigned_to TEXT,
  license_type TEXT NOT NULL,
  serial_number TEXT,
  start_date DATE,
  end_date DATE
);