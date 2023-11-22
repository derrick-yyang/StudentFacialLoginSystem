import cv2
import pickle
import os
from datetime import datetime
from database import database_utils 
import tkinter as tk
from datetime import datetime, timedelta
from gui.gui_utils import CourseInformationWindow, CourseScheduleWindow, WelcomeWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def start_login():
        # 1 Create database connection
        db = database_utils.DatabaseUtils(host="localhost", user="root", password="", database="facerecognition")
        date = datetime.utcnow()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        name = 'Derrick' # TODO: Remove this after camera recognition is accurate


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
        
        # Get the screen width and height
        screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Calculate the position to center the window
        window_x = int((screen_width - 1300) / 2)
        window_y = int((screen_height - 800) / 2)

        # Create a named window
        cv2.namedWindow('Attendance System', cv2.WINDOW_NORMAL)

        # Move the window to the center of the screen
        cv2.moveWindow('Attendance System', window_x, window_y)

        GUI_CONFIDENCE = 0 # Set confidence rate to 0 for demo purposes

        # start face recognition
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            win_started = False

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
                    # name = labels[id_]
                    current_name = name
                    color = (255, 0, 0)
                    stroke = 2
                    cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

                    # Find the student's information in the database.
                    select = "SELECT student_id, student_name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Students WHERE student_name='%s'" % (name)
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

                        update =  "UPDATE Students SET login_date=CURDATE() WHERE student_name='{}'".format(name)
                        db.execute_update_query(update)
                        update = "UPDATE Students SET login_time=NOW() WHERE student_name='{}'".format(name)
                        db.execute_update_query(update)
                    
                        hello = ("Hello ", current_name, "You did attendance today")
                        print(hello)
                        cv2.destroyAllWindows()
                        get_login_time = "SELECT login_time FROM Students WHERE student_name='{}'".format(name)
                        login_time = db.execute_query(get_login_time)
                        login_time = login_time[0][0].strftime('%b %d, %Y %H:%M:%S')

                        now = datetime.now()

                        ws = WelcomeWindow(name, login_time)
                        ws.render()

                        next_class_time = db.getNextClassStartTime(name)
                        if next_class_time != '-1':
                            next_start_class_time = datetime.strptime(next_class_time, "%H:%M:%S").time()
                            next_class_time = datetime.combine(now.date(), next_start_class_time)

                        # If there is no class today or class isnt in the next hour
                        if next_class_time == '-1' or not (now <= next_class_time <= now + timedelta(hours=1)):
                            schedule = db.getClassSchedule(name)
                            cs = CourseScheduleWindow(name, schedule)
                            cs.render()

                        # If there is class in the next hour...
                        else:
                            class_info = db.getNextClassInfo(name)
                            ci = CourseInformationWindow(name, course_details=class_info)
                            ci.render()
                        
                        win_started = True
                        
                        # Set logout_time
                        update = "UPDATE Students SET logout_time=NOW() WHERE student_name='{}'".format(name)
                        db.execute_update_query(update)
                        
                        break

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
            if k == ord('q') or win_started:
                break

        cap.release()
        cv2.destroyAllWindows()

def main():
    # Define login interface
    root = tk.Tk()
    root.title('Welcome!')
    
    # Set the window's size and position
    window_width = 640
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Set the window's background color
    root.configure(bg='white')

    def button_click():
        root.destroy()
        start_login()

    alertButton = tk.Button(root, text="Login", bg="black", fg="dark green", font=("Helvetica", 15, "bold"), 
                   command=button_click, bd=0, padx=20, pady=7, borderwidth=0)
    
    alertButton.pack(pady=25)

    message = tk.Label(root, text="Hello! Welcome to the Intelligent Course Management System. Click Login to Start Facial Login.",
                       bg='white', fg='black', font=('Helvetica', 12))
    message.pack(pady=20)

    root.mainloop()

    # Wait until login button is clicked
    while True:
        try:
            tk.Tk.winfo_exists(root)
        except tk.TclError:
            break
    
if __name__ == '__main__':
    main()
