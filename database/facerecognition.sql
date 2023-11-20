CREATE TABLE IF NOT EXISTS Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    login_time TIMESTAMP NOT NULL,
    logout_time TIMESTAMP NOT NULL
    login_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_name VARCHAR(100) NOT NULL,
    teacher_email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_description TEXT,
    teacher_id INT,
    lecture_notes TEXT,
    FOREIGN KEY(teacher_id) REFERENCES Teachers(teacher_id)
);

CREATE TABLE IF NOT EXISTS Classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    day_of_week VARCHAR(15),
    start_time TIME,
    end_time TIME,
    classroom VARCHAR(50),
    zoom_link VARCHAR(200),
    FOREIGN KEY(course_id) REFERENCES Courses(course_id)
);

CREATE TABLE IF NOT EXISTS StudentClass (
    student_class_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES Students(student_id),
    FOREIGN KEY(class_id) REFERENCES Classes(class_id)
);

