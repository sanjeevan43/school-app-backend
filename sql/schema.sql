-- Database Schema for School Transport Management System

-- Admins Table
CREATE TABLE IF NOT EXISTS admins (
    admin_id VARCHAR(36) PRIMARY KEY,
    phone BIGINT NOT NULL UNIQUE,
    email VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Parents Table
CREATE TABLE IF NOT EXISTS parents (
    parent_id VARCHAR(36) PRIMARY KEY,
    phone BIGINT NOT NULL UNIQUE,
    email VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    parent_role VARCHAR(20) DEFAULT 'GUARDIAN',
    door_no VARCHAR(50),
    street VARCHAR(100),
    city VARCHAR(50),
    district VARCHAR(50),
    pincode VARCHAR(10),
    parents_active_status VARCHAR(20) DEFAULT 'ACTIVE',
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Drivers Table
CREATE TABLE IF NOT EXISTS drivers (
    driver_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone BIGINT NOT NULL UNIQUE,
    email VARCHAR(255),
    licence_number VARCHAR(50),
    licence_expiry DATE,
    password_hash VARCHAR(255) NOT NULL,
    fcm_token VARCHAR(255),
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Routes Table
CREATE TABLE IF NOT EXISTS routes (
    route_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    routes_active_status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Route Stops Table
CREATE TABLE IF NOT EXISTS route_stops (
    stop_id VARCHAR(36) PRIMARY KEY,
    route_id VARCHAR(36) NOT NULL,
    stop_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    pickup_stop_order INT,
    drop_stop_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE
);

-- Buses Table
CREATE TABLE IF NOT EXISTS buses (
    bus_id VARCHAR(36) PRIMARY KEY,
    registration_number VARCHAR(20) NOT NULL UNIQUE,
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
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE SET NULL,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE SET NULL
);

-- Classes Table
CREATE TABLE IF NOT EXISTS classes (
    class_id VARCHAR(36) PRIMARY KEY,
    class_name VARCHAR(20) NOT NULL,
    section VARCHAR(10) NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_class (class_name, section, academic_year)
);

-- Students Table
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(36) PRIMARY KEY,
    parent_id VARCHAR(36) NOT NULL,
    s_parent_id CHAR(36) DEFAULT NULL,
    name VARCHAR(100) NOT NULL,
    dob DATE,
    study_year VARCHAR(20) NOT NULL,
    class_id VARCHAR(36),
    pickup_route_id VARCHAR(36),
    drop_route_id VARCHAR(36),
    pickup_stop_id VARCHAR(36),
    drop_stop_id VARCHAR(36),
    emergency_contact BIGINT,
    student_photo_url VARCHAR(200),
    is_transport_user BOOLEAN DEFAULT TRUE,
    student_status VARCHAR(20) DEFAULT 'CURRENT',
    transport_status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES parents(parent_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE SET NULL,
    FOREIGN KEY (pickup_route_id) REFERENCES routes(route_id) ON DELETE SET NULL,
    FOREIGN KEY (drop_route_id) REFERENCES routes(route_id) ON DELETE SET NULL,
    FOREIGN KEY (pickup_stop_id) REFERENCES route_stops(stop_id) ON DELETE SET NULL,
    FOREIGN KEY (drop_stop_id) REFERENCES route_stops(stop_id) ON DELETE SET NULL
);

-- Trips Table
CREATE TABLE IF NOT EXISTS trips (
    trip_id VARCHAR(36) PRIMARY KEY,
    bus_id VARCHAR(36) NOT NULL,
    driver_id VARCHAR(36) NOT NULL,
    route_id VARCHAR(36) NOT NULL,
    trip_date DATE NOT NULL,
    trip_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'NOT_STARTED',
    current_stop_order INT DEFAULT 0,
    started_at TIMESTAMP NULL,
    ended_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (bus_id) REFERENCES buses(bus_id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE
);

-- FCM Tokens Table
CREATE TABLE IF NOT EXISTS fcm_tokens (
    fcm_id VARCHAR(36) PRIMARY KEY,
    fcm_token VARCHAR(255) NOT NULL UNIQUE,
    student_id VARCHAR(36),
    parent_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES parents(parent_id) ON DELETE CASCADE
);

-- Error Logs Table
CREATE TABLE IF NOT EXISTS error_logs (
    error_id VARCHAR(36) PRIMARY KEY,
    error_type VARCHAR(50),
    error_code INT,
    error_description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Driver Live Locations Table
CREATE TABLE IF NOT EXISTS driver_live_locations (
    driver_id VARCHAR(36) PRIMARY KEY,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id) ON DELETE CASCADE
);
