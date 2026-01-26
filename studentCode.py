
# The code provided is an example for students to follow and should be replaced with your code. The script
# will execute all of the SQL code in each of these two variables.
#
# The structure of the SQLAndNameTableCode variable is tableName: creationSQL-code.
#
# If the SQLAndNameTableCode code is correct and syntax error free, it should be executed sequentially for
# each table entry, followed by the statements in the table data entry statements (sqlDataStatements).
#
# The sqlDataStatements variable is a list of SQL statements meant to populate the tables that were built using the
# SQL in the previous variable (SQLAndNameTableCode)
#
# Example code is given below and can be used to test your installation. You should then replace it with your
# design's code once you know everything is running smoothly.



SQLAndNameTableCode = {
    "Teacher": """CREATE TABLE IF NOT EXISTS Teacher (
        teacher_id    INT UNSIGNED NOT NULL AUTO_INCREMENT,
        first_name    VARCHAR(50)  NOT NULL,
        last_name     VARCHAR(50)  NOT NULL,
        email         VARCHAR(255) NOT NULL,
        subject_area  VARCHAR(100) NOT NULL,
        hire_date     DATE         NOT NULL,
        PRIMARY KEY (teacher_id),
        UNIQUE KEY uq_teacher_email (email)
    );""",

    "Classroom": """CREATE TABLE IF NOT EXISTS Classroom (
        classroom_id   INT UNSIGNED NOT NULL AUTO_INCREMENT,
        room_number    VARCHAR(20)  NOT NULL,
        building_name  VARCHAR(100) NOT NULL,
        grade_level    TINYINT UNSIGNED NOT NULL,
        capacity       SMALLINT UNSIGNED NOT NULL,
        PRIMARY KEY (classroom_id),
        UNIQUE KEY uq_classroom_location (building_name, room_number),
        CHECK (grade_level BETWEEN 0 AND 12)
    );""",

    "School_Administrator": """CREATE TABLE IF NOT EXISTS School_Administrator (
        admin_id     INT UNSIGNED NOT NULL AUTO_INCREMENT,
        first_name   VARCHAR(50)  NOT NULL,
        last_name    VARCHAR(50)  NOT NULL,
        role         VARCHAR(100) NOT NULL,
        email        VARCHAR(255) NOT NULL,
        PRIMARY KEY (admin_id),
        UNIQUE KEY uq_admin_email (email)
    );""",

    "Student": """CREATE TABLE IF NOT EXISTS Student (
        student_id        INT UNSIGNED NOT NULL AUTO_INCREMENT,
        first_name        VARCHAR(50)  NOT NULL,
        last_name         VARCHAR(50)  NOT NULL,
        date_of_birth     DATE         NOT NULL,
        grade_level       TINYINT UNSIGNED NOT NULL,
        enrollment_year   SMALLINT UNSIGNED NOT NULL,
        PRIMARY KEY (student_id),
        CHECK (grade_level BETWEEN 0 AND 12)
    );""",

    "Course": """CREATE TABLE IF NOT EXISTS Course (
        course_id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
        course_name    VARCHAR(150) NOT NULL,
        subject        VARCHAR(100) NOT NULL,
        grade_level    TINYINT UNSIGNED NOT NULL,
        academic_year  VARCHAR(9)   NOT NULL,
        teacher_id     INT UNSIGNED NOT NULL,
        classroom_id   INT UNSIGNED NOT NULL,
        PRIMARY KEY (course_id),
        CONSTRAINT fk_course_teacher
            FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
        CONSTRAINT fk_course_classroom
            FOREIGN KEY (classroom_id) REFERENCES Classroom(classroom_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
        CHECK (grade_level BETWEEN 0 AND 12)
    );""",

    "IoT_Device": """CREATE TABLE IF NOT EXISTS IoT_Device (
        device_id     INT UNSIGNED NOT NULL AUTO_INCREMENT,
        device_type   VARCHAR(50)  NOT NULL,
        device_name   VARCHAR(100) NOT NULL,
        status        VARCHAR(20)  NOT NULL,
        classroom_id  INT UNSIGNED NOT NULL,
        admin_id      INT UNSIGNED NOT NULL,
        PRIMARY KEY (device_id),
        CONSTRAINT fk_device_classroom
            FOREIGN KEY (classroom_id) REFERENCES Classroom(classroom_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
        CONSTRAINT fk_device_admin
            FOREIGN KEY (admin_id) REFERENCES School_Administrator(admin_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
    );""",

    "Student_Course": """CREATE TABLE IF NOT EXISTS Student_Course (
        student_id     INT UNSIGNED NOT NULL,
        course_id      INT UNSIGNED NOT NULL,
        enrolled_on    DATE         NOT NULL DEFAULT (CURRENT_DATE),
        PRIMARY KEY (student_id, course_id),
        INDEX idx_sc_course (course_id),
        CONSTRAINT fk_sc_student
            FOREIGN KEY (student_id) REFERENCES Student(student_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        CONSTRAINT fk_sc_course
            FOREIGN KEY (course_id) REFERENCES Course(course_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );""",	
}

sqlDataStatements = [
    f"INSERT INTO Teacher (first_name, last_name, email, subject_area, hire_date) VALUES ('Sarah', 'Anderson', 's.anderson@school.edu', 'Mathematics', '2018-08-15')",
    f"INSERT INTO Teacher (first_name, last_name, email, subject_area, hire_date) VALUES ('David', 'Miller', 'd.miller@school.edu', 'Science', '2020-01-10')",
    f"INSERT INTO Classroom (room_number, building_name, grade_level, capacity) VALUES ('101', 'Main Building', 5, 30)",
    f"INSERT INTO Classroom (room_number, building_name, grade_level, capacity) VALUES ('202', 'Science Wing', 6, 28)",
	f"INSERT INTO School_Administrator (first_name, last_name, role, email) VALUES ('Michael', 'Reynolds', 'Principal', 'm.reynolds@school.edu')",
    f"INSERT INTO School_Administrator (first_name, last_name, role, email) VALUES ('Laura', 'Chen', 'IT Administrator', 'l.chen@school.edu')",
    f"INSERT INTO School_Administrator (first_name, last_name, role, email) VALUES ('Robert', 'Singh', 'Facilities Manager', 'r.singh@school.edu')",
    f"INSERT INTO Student (first_name, last_name, date_of_birth, grade_level, enrollment_year) VALUES ('Emma', 'Johnson', '2012-03-15', 5, 2025)", 
    f"INSERT INTO Student (first_name, last_name, date_of_birth, grade_level, enrollment_year) VALUES ('Liam', 'Brown', '2011-07-22', 6, 2025)",
    f"INSERT INTO Course (course_name, subject, grade_level, academic_year, teacher_id, classroom_id) VALUES ('Advanced Math', 'Mathematics', 5, '2025-2026', 1, 1)",
    f"INSERT INTO Course (course_name, subject, grade_level, academic_year, teacher_id, classroom_id) VALUES ('Earth Science', 'Science', 6, '2025-2026', 2, 2)",
	f"INSERT INTO Student_Course (student_id, course_id) VALUES (1, 1)",
    f"INSERT INTO Student_Course (student_id, course_id) VALUES (2, 2)",    
    f"INSERT INTO IoT_Device (device_type, device_name, status, classroom_id, admin_id) VALUES ('smart_board', 'Smart Board A101', 'active', 1, 2)",
    f"INSERT INTO IoT_Device (device_type, device_name, status, classroom_id, admin_id) VALUES ('camera', 'Security Camera A101', 'active', 1, 3)",
    f"INSERT INTO IoT_Device (device_type, device_name, status, classroom_id, admin_id) VALUES ('speaker', 'PA Speaker B202', 'maintenance', 2, 3)",
    f"INSERT INTO IoT_Device (device_type, device_name, status, classroom_id, admin_id) VALUES ('smart_board', 'Smart Board B202', 'active', 2, 2)",     
    f"INSERT INTO IoT_Device (device_type, device_name, status, classroom_id, admin_id) VALUES ('camera', 'Hallway Camera Main', 'inactive', 1, 2)",
	f"INSERT INTO  Student_Course (student_id, course_id) VALUES (1, 1)",
	f"INSERT INTO  Student_Course (student_id, course_id) VALUES (2, 2)",
]




