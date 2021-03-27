from ics import Calendar
import requests

# Title = [CSC 236] LINKHLL

class Task:
    # Self, Title which includes the name of the class and title of event
    # notes includes the actual due TIME and the event notes and links
    # due is the date 
    def __init__(self, title, notes, due):
        self.title = title
        self.notes = notes
        self.due = due

def createCalendarURL(url):
    return Calendar(requests.get(url).text)

def createCalendarFile(file):
    f = open(file,"r")
    return Calendar(f.read())

def getEvents(calendar):
    return calendar.events

def getTasks(events, style):
    list = []
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
        print(name)
        notes = "DUE @ " + event.end.shift(hours=-4).format("h:mm a")
        print(" - " + notes)
        t = Task(name, event.description, event.end.isoformat)
        list.append(t)

def main():
    cal = createCalendarURL("https://moodle-courses2021.wolfware.ncsu.edu/calendar/export_execute.php?userid=138996&authtoken=25051e72c7311e1a04bdf806ec0af99ffea47dcf&preset_what=all&preset_time=custom")
    # print(getEvents(cal))
    # cal = createCalendarFile("../test-files/icalexport.ics")
    getTasks(getEvents(cal), 1)
    # print(getEvents(cal))
    # for event in getEvents(cal):
    #     print(event.name)
    #     print(event.end.isoformat())
    #     print(event.description)
    #     for cat in event.categories:
    #         print(cat)
    
    
if __name__ == '__main__':
    main()