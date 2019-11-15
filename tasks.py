
import datetime

class Task:
    total_time = 0
    total_minutes = "0"
    total_hours = "0"
    date = datetime.datetime.now()
    summary = [] #the title of the task
    duration = ""
    date = ""

    def __init__(self, name, start_time, end_time,color):
        self.name = name
        self.color = color
        self.start_time = start_time
        self.end_time = end_time

    def addSummary(self, summary):
        self.summary.append(summary)


    def setMinutes(self, minutes):
        self.total_minutes = minutes

    def setHours(self, hours):
        self.total_hours = hours

    def setDate(self, date):
        self.date = date

        #making calculations to see how long is the task
    def get_time_of_task(self):
        start = self.start_time.split(":") #E.g. 17:00:00 into an array [0] = 17, [1] = 00, [2] = 00
        end = self.end_time.split(":") #same thing as in start
        start_hour = self.make_int(str(start[0])) #E.g. 17
        start_minutes = self.make_int(str(start[1])) #E.g 00

        #grabbing the ending time
        end_hour = self.make_int(str(end[0]))
        end_minutes = self.make_int(str(end[1]))

        start_is_greater = False
        extra = 0

        if start_minutes > 0:
            start_hour += 1
            start_is_greater = True

        time = end_hour - start_hour
        if time < 0:
            time = time*-1 #making it positive
        if start_is_greater:
            extra = 60-start_minutes
        time = ((time*60) + extra + end_minutes)/60.0
        self.total_time = time




        #if start_minutes > 0:
            #print("Greater")
        #time = end_hour - start_hour
        #print(time, "hours spent on this task")
        #if time < 0 :
            #time = time*-1


    def make_int(self, time):
        arr = []
        for line in time:
            if line.strip():
                try:
                    n = int(line)
                    arr.append(n)
                except Exception as e:
                    pass
        hour_string = str(arr[0]) + str(arr[1])
        int_hour = int(hour_string)
        return int_hour
