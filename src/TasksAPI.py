import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from CalendarAPI import *

SCOPES = ['https://www.googleapis.com/auth/tasks']

def checkAuth():
    creds = None

    print(os.path.exists('../resources/token.json'))

    if os.path.exists('../resources/token.json'):
        creds = Credentials.from_authorized_user_file('../resources/token.json', SCOPES)
    
    if not creds or not creds.valid:
        print(creds)
        print(creds.valid)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../resources/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../resources/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('tasks', 'v1', credentials=creds)

    return service

def view(service):
    tasklist = service.tasks().list(tasklist='@default', maxResults = 10).execute()

    task_list = tasklist.get('items', [])

    task_list_final = []

    for task in task_list:
        t = Task(task['title'], task['notes'], task['due'])
        task_list_final.append(t)

    return task_list_final

def checkDuplicate(service, task):
    # Gets a list of the tasks to see if they exist or not
    gettasks = service.tasks().list(tasklist='@default', showCompleted=True, showHidden=True, maxResults=100).execute()

    found = False
    dateTimeChange = False
    idNum = None

    tasks_final = gettasks.get('items', [])

    for tsk in tasks_final:
        idNum = tsk['id']
        if tsk['title'] == task.title:
            if tsk['due'][:10] != task.due[:10]:
                dateTimeChange = True
                break
            found = True
            break

    gettasks = service.tasks().list(tasklist='@default', showCompleted = False, showHidden = False, maxResults = 100).execute()

    tasks_final = gettasks.get('items', [])
    
    if not found:
        for tsk in tasks_final:
            print(task.title.find(tsk['title'][9:]))
            print(task.title.find(tsk['title'][8:]))
            print("\n\n")
            if task.title.find(tsk['title'][8:]) != -1 or task.title.find(tsk['title'][9:]) != -1:
                dateTimeChange = True
                idNum = tsk['id']
                break

    return idNum, found, dateTimeChange

def addTask(service, task):

    idNum, doNotAdd, dateTimeChange = checkDuplicate(service, task)

    if dateTimeChange:
        removeTask(service, task, idNum)

    if doNotAdd:
        return
        
    add = {
        'title' : task.title,
        'notes' : task.notes,
        'due' : task.due
    }

    result = service.tasks().insert(tasklist='@default', body=add).execute()
    

def removeTask(service,task,taskid):
    service.tasks().delete(tasklist='@default', task=taskid).execute()

def addAllTasks(service, tasks):
    for task in tasks:
        addTask(service, task)

def main():
    service = checkAuth()
    #addTask(service, Task('Testing Automation', 'Some notes', '2021-03-28T00:00:00.000Z'))
    addAllTasks(service, getTasksFromCalendar(False, "../test-files/icalexport.ics", 0))

if __name__ == '__main__':
    main()