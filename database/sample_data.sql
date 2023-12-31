INSERT INTO Students(student_name, login_time, logout_time, login_date)
VALUES('Derrick', NOW(), NOW(), CURDATE());

INSERT INTO Teachers(teacher_name, teacher_email)
VALUES('John Doe', 'johndoe@email.com');

SET @courseTeacherId = LAST_INSERT_ID();

INSERT INTO Courses(course_name, course_description, teacher_id, lecture_notes)
VALUES('Introduction to Databases', 'This is a beginner course for databases', @courseTeacherId, 'Note 1');

SET @courseId = LAST_INSERT_ID();

INSERT INTO Classes(course_id, day_of_week, start_time, end_time, classroom, zoom_link)
VALUES(@courseId, 'Wednesday', '00:00:00', '23:00:00', 'Room 101', 'https://zoom.us');

INSERT INTO Classes(course_id, day_of_week, start_time, end_time, classroom, zoom_link)
VALUES(@courseId, 'Thursday', '23:30:00', '00:00:00', 'Room 102', 'https://zoom.us');

INSERT INTO Classes(course_id, day_of_week, start_time, end_time, classroom, zoom_link)
VALUES(@courseId, 'Tuesday', '23:00:00', '23:59:00', 'Room 103', 'https://zoom.us');

SET @studentId = (SELECT student_id FROM Students WHERE student_name = 'Derrick');

SET @classId1 = (SELECT class_id FROM Classes WHERE day_of_week = 'Tuesday' AND course_id = @courseId);
SET @classId2 = (SELECT class_id FROM Classes WHERE day_of_week = 'Thursday' AND course_id = @courseId);
SET @classId3 = (SELECT class_id FROM Classes WHERE day_of_week = 'Wednesday' AND course_id = @courseId);

INSERT INTO StudentClass(student_id, class_id)
VALUES(@studentId, @classId1), (@studentId, @classId2), (@studentId, @classId3);