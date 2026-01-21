-- 1. Create Database
CREATE DATABASE IF NOT EXISTS dualkey_db;
USE dualkey_db;

-- 2. Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL, -- In production, store hashes!
    role ENUM('ADMIN', 'SERVICE', 'AUDITOR') NOT NULL
);

-- 3. Create System Keys Table (Stores Kyber Keys)
CREATE TABLE IF NOT EXISTS system_keys (
    key_id VARCHAR(100) PRIMARY KEY,
    public_key BLOB NOT NULL,
    private_key BLOB NOT NULL
);

-- 4. Create Ledger Table (Blockchain)
CREATE TABLE IF NOT EXISTS ledger (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `index` INT UNIQUE NOT NULL,
    timestamp VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    key_id VARCHAR(100),
    user_id VARCHAR(50),
    data_reference VARCHAR(255),
    previous_hash VARCHAR(64) NOT NULL,
    hash VARCHAR(64) NOT NULL
);

-- 5. Seed Initial Users (If not exists)
INSERT IGNORE INTO users (username, password, role) VALUES 
('admin', 'password', 'ADMIN'),
('service', 'password', 'SERVICE'),
('auditor', 'password', 'AUDITOR'),
('Mithun', 'password', 'ADMIN');

-- 6. View All Tables
-- View Users
SELECT * FROM users;

-- View System Keys (Public/Private keys are binary blobs)
SELECT key_id, HEX(public_key) as public_key_hex FROM system_keys;

-- View Blockchain Ledger
SELECT * FROM ledger ORDER BY `index` ASC;
