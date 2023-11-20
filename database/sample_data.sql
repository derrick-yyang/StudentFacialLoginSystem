-- Insert a student named Derrick
INSERT INTO Students (student_name, login_time, logout_time)
VALUES ('Derrick', NOW(), NOW());

-- Insert a teacher (we need a teacher before we can create a course)
INSERT INTO Teachers (teacher_name, teacher_email)
VALUES ('John Doe', 'johndoe@example.com');

-- Get the ID of the teacher we just inserted
SET @teacher_id = (SELECT teacher_id FROM Teachers WHERE teacher_name = 'John Doe');

-- Insert a course called "Introduction to Databases"
INSERT INTO Courses (course_name, course_description, teacher_id, lecture_notes)
VALUES ('Introduction to Databases', 'This is a course about databases.', @teacher_id, 'Lecture notes for the course');

-- Get the ID of the course we just inserted
SET @course_id = (SELECT course_id FROM Courses WHERE course_name = 'Introduction to Databases');

-- Insert two classes that happen at 2:30pm - 3:30pm on Tuesday and Thursday
INSERT INTO Classes (course_id, day_of_week, start_time, end_time, classroom, zoom_link)
VALUES (@course_id, 'Tuesday', '14:00:00', '15:00:00', 'Room 101', 'https://zoom.us/j/1234567890'),
       (@course_id, 'Thursday', '14:00:00', '15:00:00', 'Room 101', 'https://zoom.us/j/1234567890');

-- Get the ID of the student we inserted earlier
SET @student_id = (SELECT student_id FROM Students WHERE student_name = 'Derrick');

-- Get the IDs of the classes we just inserted
SET @class_id_tuesday = (SELECT class_id FROM Classes WHERE zoom_link = 'https://zoom.us/j/1234567890' AND day_of_week = 'Tuesday');
SET @class_id_thursday = (SELECT class_id FROM Classes WHERE zoom_link = 'https://zoom.us/j/1234567890' AND day_of_week = 'Thursday');

-- Enroll Derrick in these two classes
INSERT INTO StudentClass (student_id, class_id)
VALUES (@student_id, @class_id_tuesday),
       (@student_id, @class_id_thursday);
