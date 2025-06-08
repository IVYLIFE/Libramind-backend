-- ========================================= [DB and User Creation] =========================================


-- Drop database if exists
DROP DATABASE IF EXISTS libramind;

-- Drop user if exists
DROP ROLE IF EXISTS skinnysky;

-- Create user
CREATE USER skinnysky WITH PASSWORD 'skinnysky';

-- Create database with owner
CREATE DATABASE libramind OWNER skinnysky;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE libramind TO skinnysky;

\c libramind


-- 1. sudo su - postgres psql          [ Login to psql console as postgres user ]
-- 2. \i app/database/sql/db.sql       [ Run the script to create DB and User/Role ]
-- 3. \i app/database/sql/tables.sql   [ Run the script to create tables and add records ]
-- 4. psql -U skinnysky -d libramind   [ Login to psql console with the created user ]
