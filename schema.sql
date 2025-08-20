-- Deletes the table if it exists, to start fresh.
DROP TABLE IF EXISTS licenses;

-- Creates the new table with all our fields.
CREATE TABLE licenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  category TEXT,
  company TEXT,
  assigned_to TEXT,
  license_type TEXT NOT NULL,
  serial_number TEXT
);