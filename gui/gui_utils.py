import tkinter as tk

class CourseScheduleWindow:
    def __init__(self, user, schedule):
        # Create tkinter window and set the size
        self.root = tk.Tk()
        self.root.title("{}'s Course Schedule".format(user))
        self.root.geometry("1300x800")

        self.schedule = schedule

    def render_schedule(self):
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
                cell = tk.Frame(frame, borderwidth=1, relief="solid")  # Create a frame with a border
                cell.grid(row=i+1, column=j+1, sticky='nsew')  # Position the frame and make it fill the grid cell
                if i == 0:
                    # Add day labels on the x-axis
                    tk.Label(cell, text=days_of_week[j]).grid(row=i, column=j+1, padx=50, pady=20)
                if j == 0 and i != 0:
                    # Add time labels on the y-axis with vertical padding
                    tk.Label(cell, text=time[i-1]).grid(row=i+1, column=j, pady=10, padx=10)
        
        # Add the courses from the given schedule
        for name in self.schedule:
            details = schedule[name]
            self.add_course(course_name=name, day=details[2], start_time=details[0], end_time=details[1], frame=frame)

    
    def add_course(self, course_name, day, start_time, end_time, frame):
        # Add a green box for a course -- This is how you add a course, make sure it's all on the hour
        course_label = tk.Label(frame, text=course_name, bg="green", width=15, wraplength=100)

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
        row_offset = 2 # offset for the columns accounted for the labelsß
        start_hour = int(start_time.split(':')[0]) + row_offset
        end_hour = int(end_time.split(':')[0]) + row_offset

        # Position the Course at it's respective day and time
        course_label.grid(row=start_hour, column=day_to_col[day], rowspan=end_hour-start_hour, sticky='nsew')
