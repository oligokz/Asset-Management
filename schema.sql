-- Main table for storing individual licenses
CREATE TABLE IF NOT EXISTS licenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  company TEXT,
  assigned_to TEXT,
  license_type TEXT NOT NULL,
  serial_number TEXT,
  start_date DATE,
  end_date DATE
);

-- Table for storing preset options
CREATE TABLE IF NOT EXISTS presets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  preset_type TEXT NOT NULL, -- 'software' or 'company'
  value TEXT NOT NULL UNIQUE
);