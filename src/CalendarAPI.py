from ics import Calendar
import requests
import arrow

# Title = [CSC 236] LINKHLL

class Task:
    # Self, Title which includes the name of the class and title of event
    # notes includes the actual due TIME and the event notes and links
    # due is the date 
    def __init__(self, title, notes, due):
        self.title = title
        self.notes = notes
        self.due = due
    
    def toString(self):
        return "Title: " + self.title + " Notes: " + self.notes + " Due: " + self.due

def createCalendarURL(url):
    return Calendar(requests.get(url).text)

def createCalendarFile(file):
    f = open(file,"r")
    return Calendar(f.read())

def getEvents(calendar):
    return calendar.events

def getTasks(events, style):
    tasklist = []
    for event in events:
        category = None
        for cat in event.categories:
            category = cat
            category = category.split(" (")[0]
            break
        if style == 0:
            category = category + ":"
            category = "".join(category.split(" "))
        elif style == 1:
            category = "[" + category + "]"
        name = category + " " + event.name.replace("is due", "")

        if event.end < arrow.utcnow():
            continue
        notes = "DUE @ " + event.end.shift(hours=-4).format("h:mm a") + "\n" + event.description
        t = Task(name, notes, event.end.format("YYYY-MM-DDTHH:mm:ss.SSS") + "Z")
        print(t.toString())
        tasklist.append(t)
    return tasklist

def getTasksFromCalendar(url, path, style):
    cal = None
    if url:
        cal = createCalendarURL(path)
    else:
        cal = createCalendarFile(path)
    events = getEvents(cal)
    tasks = getTasks(events, style)
    return tasks
            
    

def main():
    cal = createCalendarURL("https://moodle-courses2021.wolfware.ncsu.edu/calendar/export_execute.php?userid=138996&authtoken=25051e72c7311e1a04bdf806ec0af99ffea47dcf&preset_what=all&preset_time=custom")
    # print(getEvents(cal))
    # cal = createCalendarFile("../test-files/icalexport.ics")
    getTasks(getEvents(cal), 1)
    
    
if __name__ == '__main__':
    main()