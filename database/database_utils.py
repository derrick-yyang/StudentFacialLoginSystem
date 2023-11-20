import mysql.connector
from collections import defaultdict

class DatabaseUtils:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __connect(self):
        self.connection = mysql.connector.connect(
            host=self.host, 
            user=self.user, 
            password=self.password, 
            database=self.database
        )
        self.cursor = self.connection.cursor()
    
    def __close(self):
        if (self.connection.is_connected()):
            self.cursor.close()
            self.connection.close()
    
    def __execute_query(self, query):
        self.__connect()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.__close()
        return result
    
    def getNextClassStartTime(self, name):
        query = """SELECT 
    C.start_time
FROM 
    Classes C
JOIN 
    StudentClass SC ON C.class_id = SC.class_id
JOIN 
    Students S ON SC.student_id = S.student_id
WHERE 
    S.student_name = '{}' AND
    C.start_time > NOW()
ORDER BY 
    C.start_time 
LIMIT 
    1;""".format(name)
        
        result = self.__execute_query(query)

        return str(result[0][0]) # Return in readable format
    
    def getClassSchedule(self, name):
        query = """SELECT 
    CO.course_name, 
    C.start_time, 
    C.end_time,
    C.day_of_week
FROM 
    Students S
JOIN 
    StudentClass SC ON S.student_id = SC.student_id
JOIN 
    Classes C ON SC.class_id = C.class_id
JOIN 
    Courses CO ON C.course_id = CO.course_id
WHERE 
    S.student_name = '{}';""".format(name)
        
        result = self.__execute_query(query) 

        class_schedule = defaultdict(list)
        for cl in result:
            # The format is {
            #   <course_name> : [<start_time>, <end_time>, <day_of_week>]
            # }
            class_schedule[cl[0]].append([str(cl[1]), str(cl[2]), cl[3]])

        return class_schedule
    
    def getNextClassInfo(self, name):
        query = """SELECT
    CO.course_name, CO.course_description,
    T.teacher_name, T.teacher_email, 
    C.start_time, C.end_time, C.classroom, C.zoom_link, 
    CO.lecture_notes
FROM 
    Classes C
JOIN 
    StudentClass SC ON C.class_id = SC.class_id
JOIN 
    Students S ON SC.student_id = S.student_id
JOIN 
    Courses CO ON C.course_id = CO.course_id
JOIN 
    Teachers T ON CO.teacher_id = T.teacher_id
WHERE 
    S.student_name = '{}' AND
    C.start_time > NOW()
ORDER BY 
    C.start_time 
LIMIT 
    1;""".format(name)
        
        result = self.__execute_query(query)

        course = result[0]
        course_details = {}
        course_details['name'] = course[0]
        course_details['Course Description'] = course[1]
        course_details['Teacher Name'] = course[2]
        course_details['Teacher Email'] = course[3]
        course_details['Start Time'] = str(course[4])
        course_details['End Time'] = str(course[5])
        course_details['Classroom'] = course[6]
        course_details['Zoom Link'] = course[7]
        course_details['Lecture Notes'] = course[8]

        return course_details
    

    

    

    



