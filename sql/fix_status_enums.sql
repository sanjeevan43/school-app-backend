-- SQL Fix for Bus Status and Parent Status
-- Run this if you are getting errors while setting bus status to SCRAP or SPARE

-- 1. Ensure bus status column is VARCHAR or has the correct ENUM values
ALTER TABLE buses MODIFY COLUMN status VARCHAR(20) DEFAULT 'ACTIVE';

-- 2. Ensure parents_active_status column is VARCHAR
ALTER TABLE parents MODIFY COLUMN parents_active_status VARCHAR(20) DEFAULT 'ACTIVE';

-- 3. Ensure routes_active_status column is VARCHAR
ALTER TABLE routes MODIFY COLUMN routes_active_status VARCHAR(20) DEFAULT 'ACTIVE';
