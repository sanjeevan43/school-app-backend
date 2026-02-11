-- Add LONG_ABSENT to the student_status ENUM in students table
ALTER TABLE students 
MODIFY COLUMN student_status ENUM('CURRENT', 'ALUMNI', 'DISCONTINUED', 'LONG_ABSENT') DEFAULT 'CURRENT';
