
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
    "School": """CREATE TABLE IF NOT EXISTS School (
        SchoolID INT UNSIGNED NOT NULL AUTO_INCREMENT,
        SchoolName VARCHAR(200) NOT NULL,
        DistrictName VARCHAR(200),
        AddressLine1 VARCHAR(200) NOT NULL,
        City VARCHAR(100) NOT NULL,
        StateCode CHAR(2) NOT NULL,
        PostalCode VARCHAR(10) NOT NULL,
        ContactEmail VARCHAR(254),
        IsActive BOOLEAN NOT NULL DEFAULT TRUE,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (SchoolID)
    ) ENGINE=InnoDB""",

    "User": """CREATE TABLE IF NOT EXISTS `User` (
        UserID INT UNSIGNED NOT NULL AUTO_INCREMENT,
        SchoolID INT UNSIGNED NOT NULL,
        FirstName VARCHAR(100) NOT NULL,
        LastName VARCHAR(100) NOT NULL,
        Email VARCHAR(254) NOT NULL,
        `Role` VARCHAR(20) NOT NULL,
        AccountStatus VARCHAR(20) NOT NULL DEFAULT 'Active',
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (UserID),
        UNIQUE KEY UQ_User_Email (Email),
        UNIQUE KEY UQ_User_School_User (SchoolID, UserID),
        KEY IX_User_School_Role (SchoolID, `Role`),
        CONSTRAINT FK_User_School
            FOREIGN KEY (SchoolID) REFERENCES School (SchoolID),
        CONSTRAINT CK_User_Role
            CHECK (`Role` IN ('Student', 'Teacher', 'Administrator')),
        CONSTRAINT CK_User_Status
            CHECK (AccountStatus IN ('Active', 'Inactive', 'Suspended'))
    ) ENGINE=InnoDB""",

    "Course": """CREATE TABLE IF NOT EXISTS Course (
        CourseID INT UNSIGNED NOT NULL AUTO_INCREMENT,
        SchoolID INT UNSIGNED NOT NULL,
        TeacherID INT UNSIGNED NOT NULL,
        CourseCode VARCHAR(30) NOT NULL,
        CourseName VARCHAR(200) NOT NULL,
        `Subject` VARCHAR(100) NOT NULL,
        GradeLevel TINYINT UNSIGNED NOT NULL,
        AcademicYear CHAR(9) NOT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (CourseID),
        UNIQUE KEY UQ_Course_School_Course (SchoolID, CourseID),
        UNIQUE KEY UQ_Course_School_Code_Year
            (SchoolID, CourseCode, AcademicYear),
        KEY IX_Course_Teacher (SchoolID, TeacherID),
        CONSTRAINT FK_Course_School
            FOREIGN KEY (SchoolID) REFERENCES School (SchoolID),
        CONSTRAINT FK_Course_Teacher
            FOREIGN KEY (SchoolID, TeacherID)
            REFERENCES `User` (SchoolID, UserID),
        CONSTRAINT CK_Course_GradeLevel
            CHECK (GradeLevel BETWEEN 0 AND 12)
    ) ENGINE=InnoDB""",

    "Enrollment": """CREATE TABLE IF NOT EXISTS Enrollment (
        EnrollmentID INT UNSIGNED NOT NULL AUTO_INCREMENT,
        SchoolID INT UNSIGNED NOT NULL,
        CourseID INT UNSIGNED NOT NULL,
        StudentID INT UNSIGNED NOT NULL,
        EnrolledAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        EnrollmentStatus VARCHAR(20) NOT NULL DEFAULT 'Active',
        FinalGrade DECIMAL(5,2),
        CompletedAt DATETIME,
        PRIMARY KEY (EnrollmentID),
        UNIQUE KEY UQ_Enrollment_School_Course_Student
            (SchoolID, CourseID, StudentID),
        UNIQUE KEY UQ_Enrollment_Course_Student (CourseID, StudentID),
        KEY IX_Enrollment_Student (SchoolID, StudentID),
        CONSTRAINT FK_Enrollment_Course
            FOREIGN KEY (SchoolID, CourseID)
            REFERENCES Course (SchoolID, CourseID),
        CONSTRAINT FK_Enrollment_Student
            FOREIGN KEY (SchoolID, StudentID)
            REFERENCES `User` (SchoolID, UserID),
        CONSTRAINT CK_Enrollment_Status
            CHECK (EnrollmentStatus IN ('Active', 'Completed', 'Dropped')),
        CONSTRAINT CK_Enrollment_FinalGrade
            CHECK (FinalGrade IS NULL OR FinalGrade BETWEEN 0 AND 100),
        CONSTRAINT CK_Enrollment_CompletedAt
            CHECK (CompletedAt IS NULL OR CompletedAt >= EnrolledAt)
    ) ENGINE=InnoDB""",

    "Assignment": """CREATE TABLE IF NOT EXISTS Assignment (
        AssignmentID INT UNSIGNED NOT NULL AUTO_INCREMENT,
        CourseID INT UNSIGNED NOT NULL,
        Title VARCHAR(200) NOT NULL,
        `Description` TEXT,
        DueAt DATETIME NOT NULL,
        MaxPoints DECIMAL(7,2) NOT NULL,
        AssignmentType VARCHAR(30) NOT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (AssignmentID),
        UNIQUE KEY UQ_Assignment_Course_Assignment
            (CourseID, AssignmentID),
        KEY IX_Assignment_Course_DueAt (CourseID, DueAt),
        CONSTRAINT FK_Assignment_Course
            FOREIGN KEY (CourseID) REFERENCES Course (CourseID),
        CONSTRAINT CK_Assignment_MaxPoints CHECK (MaxPoints > 0)
    ) ENGINE=InnoDB""",

    "Submission": """CREATE TABLE IF NOT EXISTS Submission (
        SubmissionID INT UNSIGNED NOT NULL AUTO_INCREMENT,
        CourseID INT UNSIGNED NOT NULL,
        AssignmentID INT UNSIGNED NOT NULL,
        StudentID INT UNSIGNED NOT NULL,
        SubmittedAt DATETIME,
        StorageUri VARCHAR(2048),
        Score DECIMAL(7,2),
        InstructorFeedback TEXT,
        SubmissionStatus VARCHAR(20) NOT NULL DEFAULT 'Draft',
        PRIMARY KEY (SubmissionID),
        UNIQUE KEY UQ_Submission_Assignment_Student
            (AssignmentID, StudentID),
        KEY IX_Submission_Assignment (CourseID, AssignmentID),
        KEY IX_Submission_Enrollment (CourseID, StudentID),
        KEY IX_Submission_Student (StudentID),
        CONSTRAINT FK_Submission_Assignment
            FOREIGN KEY (CourseID, AssignmentID)
            REFERENCES Assignment (CourseID, AssignmentID),
        CONSTRAINT FK_Submission_Enrollment
            FOREIGN KEY (CourseID, StudentID)
            REFERENCES Enrollment (CourseID, StudentID),
        CONSTRAINT CK_Submission_Score
            CHECK (Score IS NULL OR Score >= 0),
        CONSTRAINT CK_Submission_Status
            CHECK (SubmissionStatus IN ('Draft', 'Submitted', 'Graded')),
        CONSTRAINT CK_Submission_SubmittedAt
            CHECK (SubmissionStatus = 'Draft' OR SubmittedAt IS NOT NULL)
    ) ENGINE=InnoDB"""
}

sqlDataStatements = [
    """INSERT INTO School
        (SchoolName, DistrictName, AddressLine1, City, StateCode,
         PostalCode, ContactEmail)
       VALUES
        ('Maple Grove School', 'North District', '100 Main Street',
         'Springfield', 'IL', '62701', 'office@maplegrove.example')""",

    """INSERT INTO `User`
        (SchoolID, FirstName, LastName, Email, `Role`)
       VALUES
        (1, 'Sarah', 'Anderson', 'sarah.anderson@maplegrove.example',
         'Teacher')""",

    """INSERT INTO `User`
        (SchoolID, FirstName, LastName, Email, `Role`)
       VALUES
        (1, 'Avery', 'Morgan', 'avery.morgan@maplegrove.example',
         'Student')""",

    """INSERT INTO Course
        (SchoolID, TeacherID, CourseCode, CourseName, `Subject`,
         GradeLevel, AcademicYear)
       VALUES
        (1, 1, 'MATH-06', 'Grade 6 Mathematics', 'Mathematics',
         6, '2026-2027')""",

    """INSERT INTO Enrollment
        (SchoolID, CourseID, StudentID)
       VALUES
        (1, 1, 2)""",

    """INSERT INTO Assignment
        (CourseID, Title, `Description`, DueAt, MaxPoints, AssignmentType)
       VALUES
        (1, 'Fractions Practice', 'Complete the fractions worksheet.',
         '2026-10-15 23:59:00', 100.00, 'Homework')""",

    """INSERT INTO Submission
        (CourseID, AssignmentID, StudentID, SubmittedAt, StorageUri,
         SubmissionStatus)
       VALUES
        (1, 1, 2, '2026-10-14 16:30:00',
         's3://yodae-submissions/example/fractions-practice.pdf',
         'Submitted')"""
]







