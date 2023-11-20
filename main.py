import mysql.connector
import cv2
import pickle
import os
from datetime import datetime
import PySimpleGUI as sg
from database import database_utils 
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def start_login():
        # 1 Create database connection
        db = database_utils.DatabaseUtils(host="localhost", user="root", password="", database="facerecognition")
        date = datetime.utcnow()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")


        #2 Load recognize and read label from model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(os.path.join(BASE_DIR, "data/train.yml"))

        labels = {"person_name": 1}
        with open(os.path.join(BASE_DIR, "data/labels.pickle"), "rb") as f:
            labels = pickle.load(f)
            labels = {v: k for k, v in labels.items()}

        # Define camera and detect face
        face_cascade = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'haarcascade/haarcascade_frontalface_default.xml'))
        cap = cv2.VideoCapture(0)
        
        GUI_CONFIDENCE = 0 # Set confidence rate to 0 for demo purposes

        # start face recognition
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                print(x, w, y, h)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                # predict the id and confidence for faces
                id_, conf = recognizer.predict(roi_gray)
                print(id_, conf)

                if conf >= GUI_CONFIDENCE:
                    font = cv2.QT_FONT_NORMAL
                    id = 0
                    id += 1
                    name = labels[id_]
                    current_name = name
                    color = (255, 0, 0)
                    stroke = 2
                    cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

                    # Find the student's information in the database.
                    select = "SELECT student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'" % (name)
                    result = db.execute_query(select)
                    # print(result)
                    data = "error"

                    for x in result:
                        data = x

                    # If the student's information is not found in the database
                    if data == "error":
                        print("The student", current_name, "is NOT FOUND in the database.")
                # If the student's information is found in the database
                    else:
                        """
                        Implement useful functions here.
                        Check the course and classroom for the student.
                            If the student has class room within one hour, the corresponding course materials
                                will be presented in the GUI.
                            if the student does not have class at the moment, the GUI presents a personal class 
                                timetable for the student.

                        """
                        print("student found")
                        # update =  "UPDATE Student SET login_date=%s WHERE name=%s"
                        # val = (date, current_name)
                        # db.execute_update_query(update, val)
                        # update = "UPDATE Student SET login_time=%s WHERE name=%s"
                        # val = (current_time, current_name)
                        # db.execute_update_query(update, val)
                    
                        # hello = ("Hello ", current_name, "You did attendance today")
                        # print(hello) 

                # If the face is unrecognized
                else: 
                    color = (255, 0, 0)
                    stroke = 2
                    font = cv2.QT_FONT_NORMAL
                    cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                    hello = ("Your face is not recognized")
                    print(hello)

            cv2.imshow('Attendance System', frame)
            k = cv2.waitKey(20) & 0xff
            if k == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

def main():
    
    # Define login interface
    name = 'Derrick'
    root = tk.Tk()
    root.title('Welcome ' + name)

    def button_click():
        root.destroy()
    
    alertButton = tk.Button(root, text='login', command=button_click)
    alertButton.pack()

    message = tk.Label(root, text="Hello! Welcome to the Intelligent Course Management System. Click Login to Start Facial Login.")
    message.pack()
    root.mainloop()

    # Wait until login button is clicked
    while True:
        try:
            tk.Tk.winfo_exists(root)
        except tk.TclError:
            start_login()
            break

    
if __name__ == '__main__':
    main()
