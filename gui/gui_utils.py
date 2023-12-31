import tkinter as tk
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import tkinter as tk
from tkinter import ttk

class WelcomeWindow:
    def __init__(self, user, login_time):
        # Create tkinter window and set the size
        self.root = tk.Tk()
        # Create a custom style for the frame with a modern look
        style = ttk.Style()
        style.configure("Modern.TFrame", background="#f2f2f2", borderwidth=10)
        self.root.title("Successfully logged in as: {}. Welcome!".format(user))
        window_height = 280
        window_width = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.user = user
        self.login_time = login_time

    def render(self):
        self.welcome_screen()
        self.root.mainloop()
    
    def welcome_screen(self):
        # Create a frame with a modern look
        frame = ttk.Frame(self.root, style="Modern.TFrame")
        frame.pack(pady=50)

        welcome_label = ttk.Label(frame, text="Welcome, {}!".format(self.user), font=("Helvetica", 24))
        welcome_label.pack(pady=(50, 20), padx=(50, 50))

        login_time_label = ttk.Label(frame, text=f"Your login time: {self.login_time}", font=("Helvetica", 16))
        login_time_label.pack(pady=(0, 50))


class CourseScheduleWindow:
    def __init__(self, user, schedule):
        # Create tkinter window and set the size
        self.root = tk.Tk()
        self.root.title("{}'s Course Schedule".format(user))
        window_height = 800
        window_width = 1300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.schedule = schedule

    def render(self):
        self.create_schedule()
        self.root.mainloop()
    
    def create_schedule(self):
        # Create a list for days of the week and time
        days_of_week = [' ', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        time = [f'{i}:00' for i in range(24)]  # This creates a list from '0:00' to '23:00'

        # Create a canvas and scrollbar
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame and put it on the canvas
        frame = tk.Frame(canvas)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # Update the scrollregion of the canvas when the size of the frame changes
        frame.bind('<Configure>', lambda _: canvas.configure(scrollregion=canvas.bbox('all')))

        # Create a grid
        for i in range(len(time)+1):
            for j in range(len(days_of_week)):
                cell = tk.Frame(frame, borderwidth=0, relief="solid")  # Create a frame with a border
                cell.grid(row=i+1, column=j+1, sticky='nsew')  # Position the frame and make it fill the grid cell
                if i == 0:
                    # Add day labels on the x-axis
                    tk.Label(cell, text=days_of_week[j]).grid(row=i, column=j+1, padx=50, pady=20)
                if j == 0 and i != 0:
                    # Add time labels on the y-axis with vertical padding
                    tk.Label(cell, text=time[i-1]).grid(row=i+1, column=j, pady=10, padx=10)
        
        # Add the courses from the given schedule
        for name in self.schedule:
            classes = self.schedule[name]
            for details in classes:
                self.add_class(course_name=name, day=details[2], start_time=details[0], end_time=details[1], frame=frame)

    
    def add_class(self, course_name, day, start_time, end_time, frame):
        # Add a green box for a course -- This is how you add a course, make sure it's all on the hour
        course_label = tk.Label(frame, text=course_name, bg="light green", width=15, wraplength=100)

        # Define the column/row based on start and end time
        # Note: It's offset by +1 due to how the cols are rendered
        day_to_col = {
            'Monday'    : 2,
            'Tuesday'   : 3,
            'Wednesday' : 4,
            'Thursday'  : 5,
            'Friday'    : 6,
            'Saturday'  : 7,
            'Sunday'    : 8
        }
        row_offset = 2 # offset for the columns accounted for the labels
        start_hour = int(start_time.split(':')[0]) + row_offset
        end_hour = int(end_time.split(':')[0]) + row_offset

        # Ensure that rowspan is at least 1
        rowspan_value = max(1, end_hour - start_hour)

        # Position the Course at it's respective day and time
        course_label.grid(row=start_hour, column=day_to_col[day], rowspan=rowspan_value, sticky='nsew')


class CourseInformationWindow:
    def __init__(self, user, course_details):
        # Create tkinter window and set the size
        self.root = tk.Tk()
        self.root.title("{}'s Upcoming Course Details".format(user))
        window_height = 800
        window_width = 1300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        self.course_details = course_details

        # Entry widgets for user to input their email and password
        self.email_entry = tk.Entry(self.root, font=("Helvetica", 16))

    def render(self):
        self.add_course_details()
        self.root.mainloop()

    def open_link(self, url):
        webbrowser.open(url)
    
    def send_email(self, frame):
        user_email = self.email_entry.get()

        # email credentials and SMTP server details
        smtp_server = 'smtp.office365.com'
        smtp_port = 587
        smtp_user = 'comp3278group31@outlook.com'
        smtp_password = 'group31project'

        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = user_email
        msg['Subject'] = 'Course Details'

        # Format the course details into the body of the email
        body = "\n".join([f"{label}: {value}" for label, value in self.course_details.items()])
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # Login to the SMTP server
                server.starttls()
                server.login(smtp_user, smtp_password)

                # Send the email
                server.sendmail(smtp_user, user_email, msg.as_string())
            
            success_message = tk.Label(frame, text=f"Email sent successfully to: {user_email}!", font=("Helvetica", 14), fg="light green")
            success_message.grid(row=2, column=0, columnspan=2, pady=10)

        except Exception as e:
            error_message = tk.Label(frame, text=f"Error sending email: {e}", font=("Helvetica", 14), fg="red")
            error_message.grid(row=2, column=0, columnspan=2, pady=10)


    def add_course_details(self):
         # Course name and title
        title_frame = tk.Frame(self.root)
        title_frame.pack(side='top', fill='x')
        title = tk.Label(title_frame, text=self.course_details['name'], font=("Helvetica", 50))
        title.pack(pady=40)

        # Create a canvas and scrollbar
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame and put it on the canvas
        frame = tk.Frame(canvas)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # Update the scrollregion of the canvas when the size of the frame changes
        frame.bind('<Configure>', lambda _: canvas.configure(scrollregion=canvas.bbox('all')))

        # Create labels and text boxes for each course information
        labels = ['Course Description', 'Teacher Name', 'Teacher Email', 'Start Time', 'End Time', 'Classroom', 'Zoom Link', 'Lecture Notes']
        for i in range(len(labels)):
            tk.Label(frame, text=labels[i]+":", font=("Helvetica", 20)).grid(row=i, column=0, sticky='', pady=15, padx=200)
            label1 = tk.Label(frame, text=self.course_details[labels[i]], font=("Helvetica", 16))
            label1.grid(row=i, column=1, sticky='', pady=10, padx=40)
            if labels[i] == 'Zoom Link':
                label1.config(cursor="hand2", fg="blue", underline=True)
                label1.bind("<Button-1>", lambda event, url=self.course_details[labels[i]]: self.open_link(url))

        # Create a frame to contain the labels and entry widgets
        info_frame = tk.Frame(frame, borderwidth=2, relief="solid")
        info_frame.grid(row=len(self.course_details), column=0, columnspan=3, pady=20, padx=350)

        email_entry_title = tk.Label(info_frame, text="Send the above course information to your email", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=3, pady=10, padx=50)
        # Entry widgets for user to input their email
        email_entry_label = tk.Label(info_frame, text="Your Email:", font=("Helvetica", 16))
        email_entry_label.grid(row=1, column=0, pady=5)

        self.email_entry = tk.Entry(info_frame, font=("Helvetica", 16))
        self.email_entry.grid(row=1, column=1, pady=5)

        # Create a button to send email
        send_email_button = tk.Button(info_frame, text="Send Email", command=lambda: self.send_email(info_frame), font=("Helvetica", 16))
        send_email_button.grid(row=1, column=2, pady=5)

# # Just for testing ~
# schedule = {
#     'Introduction to Databases' : ["9:00", "10:00", 'Tuesday'],
#     'COMP 3330' : ["4:00", "10:00", 'Sunday']
# }

# course_details = {}
# course_details['name'] = "Introduction to Databases"
# course_details['Course Description'] = "alsjdlasdjfladsfkasdjfksdjlksd"
# course_details['Teacher Name'] = "Teacher name"
# course_details['Teacher Email'] = "teachername@gmail.com"
# course_details['Start Time'] = "14:00:00"
# course_details['End Time'] = "15:00:00"
# course_details['Classroom'] = "Room 10023"
# course_details['Zoom Link'] = "https://zoom.us/j/1234567890"
# course_details['Lecture Notes'] = "Lecture notes for the course"

# ci = CourseInformationWindow('Derrick', course_details=course_details)
# ci.render()
