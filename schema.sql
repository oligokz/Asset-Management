-- Main table for all assets
IF OBJECT_ID(N'dbo.assets', N'U') IS NULL
CREATE TABLE assets (
    id INT PRIMARY KEY IDENTITY(1,1),
    asset_tag NVARCHAR(255) NOT NULL UNIQUE,
    name NVARCHAR(255) NOT NULL,
    category NVARCHAR(100),
    status NVARCHAR(100),
    location NVARCHAR(255),
    purchase_date DATE,
    purchase_cost DECIMAL(10, 2),
    serial_number NVARCHAR(255),
    notes NVARCHAR(MAX)
);
GO

-- Table to track the history of an asset (check-in/check-out)
IF OBJECT_ID(N'dbo.asset_history', N'U') IS NULL
CREATE TABLE asset_history (
    id INT PRIMARY KEY IDENTITY(1,1),
    asset_id INT NOT NULL,
    status NVARCHAR(100),
    notes NVARCHAR(MAX),
    timestamp DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (asset_id) REFERENCES assets (id)
);
GO