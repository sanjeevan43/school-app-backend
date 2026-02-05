-- School Transport Management Database Schema
-- Run this script to create all required tables

CREATE DATABASE IF NOT EXISTS school_DB;
USE school_DB;

-- Admins table
CREATE TABLE IF NOT EXISTS admins (
    admin_id VARCHAR(36) PRIMARY KEY,
    phone BIGINT UNIQUE NOT NULL,
    email VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Parents table
CREATE TABLE IF NOT EXISTS parents (
    parent_id VARCHAR(36) PRIMARY KEY,
    phone BIGINT UNIQUE NOT NULL,
    email VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    parent_role ENUM('FATHER', 'MOTHER', 'GUARDIAN') DEFAULT 'GUARDIAN',
    door_no VARCHAR(50),
    street VARCHAR(100),
    city VARCHAR(50),
    district VARCHAR(50),
    pincode VARCHAR(10),
    parents_active_status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Drivers table
CREATE TABLE IF NOT EXISTS drivers (
    driver_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone BIGINT UNIQUE NOT NULL,
    email VARCHAR(255),
    licence_number VARCHAR(50),
    licence_expiry DATE,
    password_hash VARCHAR(255) NOT NULL,
    fcm_token VARCHAR(255),
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Routes table
CREATE TABLE IF NOT EXISTS routes (
    route_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    routes_active_status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Buses table (remove foreign key constraints)
CREATE TABLE IF NOT EXISTS buses (
    bus_id VARCHAR(36) PRIMARY KEY,
    registration_number VARCHAR(20) UNIQUE NOT NULL,
    driver_id VARCHAR(36),
    route_id VARCHAR(36),
    vehicle_type VARCHAR(50),
    bus_brand VARCHAR(100),
    bus_model VARCHAR(100),
    seating_capacity INT NOT NULL,
    rc_expiry_date DATE,
    fc_expiry_date DATE,
    rc_book_url VARCHAR(255),
    fc_certificate_url VARCHAR(255),
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Classes table
CREATE TABLE IF NOT EXISTS classes (
    class_id VARCHAR(36) PRIMARY KEY,
    class_name VARCHAR(20) NOT NULL,
    section VARCHAR(10) NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Route stops table (remove foreign key)
CREATE TABLE IF NOT EXISTS route_stops (
    stop_id VARCHAR(36) PRIMARY KEY,
    route_id VARCHAR(36) NOT NULL,
    stop_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    pickup_stop_order INT NOT NULL,
    drop_stop_order INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table (remove foreign key constraints that cause issues)
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(36) PRIMARY KEY,
    parent_id VARCHAR(36) NOT NULL,
    s_parent_id VARCHAR(36),
    name VARCHAR(100) NOT NULL,
    dob DATE,
    class_id VARCHAR(36),
    pickup_route_id VARCHAR(36),
    drop_route_id VARCHAR(36),
    pickup_stop_id VARCHAR(36),
    drop_stop_id VARCHAR(36),
    emergency_contact BIGINT,
    student_photo_url VARCHAR(200),
    student_status ENUM('CURRENT', 'ALUMNI', 'DISCONTINUED') DEFAULT 'CURRENT',
    transport_status ENUM('ACTIVE', 'TEMP_STOP', 'CANCELLED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Trips table (remove foreign keys)
CREATE TABLE IF NOT EXISTS trips (
    trip_id VARCHAR(36) PRIMARY KEY,
    bus_id VARCHAR(36) NOT NULL,
    driver_id VARCHAR(36) NOT NULL,
    route_id VARCHAR(36) NOT NULL,
    trip_date DATE NOT NULL,
    trip_type ENUM('MORNING', 'EVENING') NOT NULL,
    status ENUM('NOT_STARTED', 'ONGOING', 'PAUSED', 'COMPLETED', 'CANCELED') DEFAULT 'NOT_STARTED',
    current_stop_order INT DEFAULT 0,
    started_at TIMESTAMP NULL,
    ended_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- FCM tokens table (remove foreign keys)
CREATE TABLE IF NOT EXISTS fcm_tokens (
    fcm_id VARCHAR(36) PRIMARY KEY,
    fcm_token VARCHAR(255) UNIQUE NOT NULL,
    student_id VARCHAR(36),
    parent_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Error handling table
CREATE TABLE IF NOT EXISTS error_handling (
    error_id VARCHAR(36) PRIMARY KEY,
    error_type VARCHAR(50),
    error_code INT,
    error_description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Route FCM cache table (remove foreign key)
CREATE TABLE IF NOT EXISTS route_stop_fcm_cache (
    route_id VARCHAR(36) PRIMARY KEY,
    stop_fcm_map JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);