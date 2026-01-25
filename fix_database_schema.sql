-- Fix Database Schema Issues
-- Run these SQL commands on your Hostinger database

-- 1. Add missing password_hash column to drivers table
ALTER TABLE drivers ADD COLUMN password_hash VARCHAR(255) NOT NULL DEFAULT '';

-- 2. Fix typo in parents table: fcm_toten -> fcm_token
ALTER TABLE parents CHANGE COLUMN fcm_toten fcm_token VARCHAR(255) DEFAULT NULL;

-- 3. Add missing fcm_token column to drivers table
ALTER TABLE drivers ADD COLUMN fcm_token VARCHAR(255) DEFAULT NULL;

-- 4. Remove extra trips_status column from trips table
ALTER TABLE trips DROP COLUMN trips_status;