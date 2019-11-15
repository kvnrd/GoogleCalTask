''' TODO: FIGURE OUT A WAY TO COME UP WITH YOUR_TIME WITH datetime OR
BY CONVERTING THEM INTO STRINGS SINCE TIME IS 60 MINUTES '''


from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tasks import Task
from datetime import timedelta


#Sort type of events by color
TOMATO = 'IMPORTANT EVENTS'
FLAMINGO = 'SCHOOL'
TANGERINE = ''
BANANA = 'STUDY'
SAGE = ''
BASIL = ''
PEACOCK = ''
BLUEBERRY = ''
LAVENDER = ''
GRAPE = ''
GRAPHITE = ''




color_palette = {
        0: TOMATO,
        1: FLAMINGO,
        2: TANGERINE,
        3: BANANA,
        4: SAGE,
        5: BASIL,
        6: PEACOCK,
        7: BLUEBERRY,
        8: LAVENDER,
        9: GRAPE,
        10: GRAPHITE,
}


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    TOTAL_TIME_HOURS = "0"
    TOTAL_TIME_MINUTES = "0"
    EVENTS_TO_GO_THROUGH = 60
    TOTAL_TIME_FOR_WEEK = 0

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    start_day = datetime.datetime.utcnow().isoformat() + 'Z'
    #now = (datetime.datetime.utcnow()- timedelta(start_day.weekday())).isoformat() + 'Z' # 'Z' indicates UTC time
    #print("now", str(now))
    end_of_week = str(datetime.datetime.utcnow() + timedelta(days=7)) + 'Z'
    print("")
    print('Getting the upcoming 10 events')
    print("LOADING.....")
    events_result = service.events().list(calendarId='primary', timeMin=start_day,
                                        maxResults=EVENTS_TO_GO_THROUGH, singleEvents=True,
                                        orderBy='startTime').execute()

    events = events_result.get('items', [])
    colors = service.colors().get(fields="event").execute()

    tasks = [] #will hold all tasks




    if not events:

        print('No upcoming events found.')
    for event in events:

        start = event['start'].get('dateTime', event['start'].get('date')) #returns date and time 24 hrs time
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event['summary']
        if start > end_of_week:
            GREATER = True
        else:
            #print("EVENT-------", event['summary'], "-------")
            time_start_array = start.split("T")
            end_start_array = end.split("T")
            date = time_start_array[0]
            total_start_times = time_start_array[1]
            start_time_hour = total_start_times[:2]
            start_time_minutes = total_start_times[3:5]
            start_time = start_time_hour + ":" + start_time_minutes
            name = event['summary']
            total_end_times = end_start_array[1]
            end_time_hours = total_end_times[:2]
            end_time_minutes = total_end_times[3:5]
            end_time = end_time_hours + ":"+ end_time_minutes




            #task in order to find the duration of the task.
            total_duration = ""
            duration_minutes = 0
            duration_hours = 0
            if end_time_minutes == "00" and start_time_minutes != "00":
                end_time_minutes = "60"
                end_time_hours = int(end_time_hours) - 1
                duration_minutes = str(int(end_time_minutes) - int(start_time_minutes))
                duration_hours = str(int(end_time_hours) - int(start_time_hour))
                if len(duration_hours) < 2:
                    duration_hours = "0" + duration_hours
                if len(duration_minutes) < 2:
                    duration_minutes = "0" + duration_minutes
            elif int(end_time_minutes) < int(start_time_minutes):
                duration_minutes = str(int(start_time_minutes) - int(end_time_minutes))
                duration_hours = str(int(end_time_hours) - int(start_time_hour))
                if len(duration_hours) < 2:
                    duration_hours = "0" + duration_hours
                if len(duration_minutes) < 2:
                    duration_minutes = "0" + duration_minutes
            else:
                duration_minutes = str(int(end_time_minutes) - int(start_time_minutes))
                duration_hours = str(int(end_time_hours) - int(start_time_hour))
                if len(duration_hours) < 2:
                    duration_hours = "0" + duration_hours
                if len(duration_minutes) < 2:
                    duration_minutes = "0" + duration_minutes

            total_duration = duration_hours + duration_minutes


            #print("EVENT-------", event['summary'], "-------")
            try:
                #print("EVENT-------", event['summary'], "-------")
                color = colors['event'][event['colorId']]['background']
                #print("NAME-----------",name, "-----------COLOR", color)
                if color == "#dc2127":
                    color = 0
                if color == "#ff887c":
                    color = 1
                if color == "#ffb878":
                    color = 2
                if color == "#fbd75b":
                    color = 3
                if color == "#7ae7bf":
                    color = 4
                if color == "#51b749":
                    color = 5
                if color == "#46d6db":
                    color = 6
                if color == "#5484ed":
                    color = 7
                if color == "#a4bdfc":
                    color = 8
                if color == "#dbadff":
                    color = 9
                if color == "#e1e1e1":
                    color = 10
            except Exception as e:
                color = 10 #default color if event has no color


            task = Task(name,start_time, end_time, color)
            #print("-------------------------------")
            #print(task.name, task.color)
            task.date = date

            #print(task.name,"on", task.date)
            task.get_time_of_task() #gets the total time for the task
            tasks.append(task)
            task.setMinutes(duration_minutes)
            task.setHours(duration_hours)
            task.setDate(date)



    '''Managed to have total time in appropriate format E.g. instead of being 8: 4 its now 08:04'''
    for i in range(11): #traversing the color color_palette
        if len(color_palette[i]) > 1: #if the value of i in color palette is not emty
            new_task = Task(color_palette[i], 0,0, i) #for each color, you create a task
            sum_of_hours = "0"
            for task in tasks:
                if task.color == i:
                    sum_of_minutes, carry = addMinutes(new_task.total_minutes, task.total_minutes)
                    sum_of_hours = str(int(task.total_hours) + carry + int(sum_of_hours))
                    sum_of_minutes = transformToTimeFormat(sum_of_minutes)
                    sum_of_hours = transformToTimeFormat(sum_of_hours)
                    #new_task.total_time += task.total_time #you add the total time of the task
                    new_task.addSummary(task.name)
            text = "For " + new_task.name + " you have planned to spend a total of: "
            num_of_spaces = 15
            num_of_spaces -= len(new_task.name)
            string_length = len(text)+num_of_spaces
            string_revised = text.ljust(string_length)
            print("\n-----------------------------------------------------")
            new_task.setHours(sum_of_hours)
            new_task.setMinutes(sum_of_minutes)
            #print(string_revised + str(new_task.total_time) + " hrs this week")
            print(string_revised + new_task.total_hours + ":"+new_task.total_minutes)

            TOTAL_TIME_MINUTES, carry1 = addMinutes(TOTAL_TIME_MINUTES, TOTAL_TIME_MINUTES)
            TOTAL_TIME_MINUTES = transformToTimeFormat(TOTAL_TIME_MINUTES)
            TOTAL_TIME_HOURS = str(int(TOTAL_TIME_HOURS) + int(new_task.total_hours) + carry1)
            print("Which Includes the following events: ")
            print("")
            for info in new_task.summary:
                print("-", info)
            new_task.summary.clear()
            print("")




    print("----------------TOTAL TIME FOR EVENTS ", TOTAL_TIME_HOURS,":",TOTAL_TIME_MINUTES,"-------------------------------")


    time_left_hours, time_left_minutes = timeLeftForToday()
    YOUR_TIME_HOURS, YOUR_TIME_MINUTES = yourTime(time_left_hours, time_left_minutes)


    print("You have... " ,YOUR_TIME_HOURS, " hours and ",YOUR_TIME_MINUTES, " minutes left for a week. FOR YOU. This is YOUR TIME")
    #print(time_left_for_the_week)




#returns how much time is left for today.
def timeLeftForToday():
    time_right_now = datetime.datetime.now().time()
    #print(time_right_now)
    time_tuple = ((23 - time_right_now.hour, 60 - time_right_now.minute))
    #print(time_tuple)
    time_left_hours = transformToTimeFormat(str(time_tuple[0]))
    time_left_minutes = transformToTimeFormat(str(time_tuple[-1]))
    return time_left_hours, time_left_minutes



#returns time left for the week including timeLeftForToday
def yourTime(time_left_hours, time_left_minutes):
    time_for_a_week_hours = str(24*6)

    time_left_for_the_week_hour = str(int(time_for_a_week_hours) + int(time_left_hours))
    time_left_for_the_week_minutes = time_left_minutes

    return time_left_for_the_week_hour, time_left_for_the_week_minutes



#creates minutes or hours with appropriate format
def transformToTimeFormat(time):
    if len(time) < 2:
        time = "0" + time

    return time



#add minutes appropriately and returns the total minutes and if theres a carry.
def addMinutes(minutes1, minutes2):
    total = 0
    total = int(minutes1) + int(minutes2)
    if total >= 60:
        total = total - 60
        total = str(total)
        return total, 1
    else:
        total = str(total)
        return total, 0


if __name__ == '__main__':
    main()
