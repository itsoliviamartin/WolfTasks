#Developed from Google examplecode: https://github.com/gsuitedevs/python-samples/blob/master/tasks/quickstart/quickstart.py
from __future__ import print_function
import pickle
import os.path
import os
import time
import datetime
import requests, sys, webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.options import Options
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Read and Write Permission for Google Tasks
SCOPES = ['https://www.googleapis.com/auth/tasks']

#Global Variables
driver = None
select = None
currentMAUnit = None
#Prefix to place infront of automaticaly added tasks, used for both adding and removeing the tasks
prefix = "AUTO: "

def main():
    if getattr(sys, 'frozen', False) :
    # running in a bundle
        chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver')

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

    #Creates an API service for Google Tasks using the Credentials in the token.pickle file
    service = build('tasks', 'v1', credentials=creds)

    #Clears the terminal and prints a welcome message
    os.system('cls||clear')
    print("=================================================================")
    print("|                    Zach's Task Manager                        |")
    print("=================================================================")

    #Prompts for user input to get action
    act = input("Would you like to [view] or [add] or [addwebassign] tasks? ")

    #If user input view, get the tasks from default list and print them
    if act == "view":
        #Retreives tasks
        tasks = service.tasks().list(tasklist='@default').execute()
        #If no tasks are found print that
        if not tasks:
            print("No tasks found")
        #Otherwise print all the tasks in the default list
        else:
            for task in tasks['items']:
                print ("Task: " + task['title'])
                date = task['due'].split("-")
                year = date[0]
                month = date[1]
                dayS = date[2].split("T")
                day = dayS[0]
                print("     Due: " + month + "-" + day + "-" + year)
        input("Press enter to continue ")
        main()
    #If the input is add, prompt for the title and due date and add it to the default list
    elif act == "add":
        tit = input("Title: ")
        date_time_str = input("Due date (MON DD YYYY  H:MMPM): ")
        date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')
        add = {
            'title' : tit,
            'notes' : "Due @ " + date_time_str.split(" ")[-1],
            'due' : date_time_obj.isoformat() + 'Z'
        }
        result = service.tasks().insert(tasklist='@default', body=add).execute()
        time.sleep(1)
        main()
        #If result is empty there was an error
        if not result:
            print('Could not add')
        #Otherwise print the result id
        else:
            print(result['id'])
    #If the input is exit, exit the program
    elif act == "exit":
        sys.exit()
    #If the input is remove, remove all tasks with the prefix in the default list
    elif act == "remove":
        fullTasks = service.tasks().list(tasklist='@default', showCompleted=True, showHidden=True, maxResults=100).execute()
        for task in fullTasks['items']:
            if prefix in task['title']:
                service.tasks().delete(tasklist='@default', task=task['id']).execute()
        print("Removed all automated tasks")
        time.sleep(1)
        main()
    #If the input is removeauth, remove the auth file and reprompt for authorization
    elif act == "removeauth":
        remove()
        main()
    #If the input is addwebassign, scrape webassign for data, get all asignments for each class and add them as tasks
    elif act == "addwebassign":
        #Opens the password file
        file = open("userpass.txt")
        #Reads the first two lines, should be unity id and password (currently in plain text)
        user = file.readline()
        pas = file.readline()
        #Optionst to run selenium in "headless" mode, disabled for now.
        #chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #driver = webdriver.Chrome(chrome_options = chrome_options)
        #Opens chrome in automated testing mode using provided chromedriver file
        driver = webdriver.Chrome("resources\\chromedriver.exe")
        driver.set_page_load_timeout("10")
        #Page to scrape data from, currently setup for ncsu webassign. This is where homework for classes are assigned.
        driver.get("https://www.webassign.net/ncsu/login.html")
        #Finds the login button on the page and clicks it
        driver.find_element_by_id("loginbtn").click()
        timeout = 10
        #Waits for the page to load and the username and password fields are visible, otherwise catches the exception
        try:
            element_present = EC.presence_of_element_located((By.NAME, 'j_username'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load.")
            time.sleep(2)
            main()
        #Uses the stored username and password values to login to webassign
        driver.find_element_by_name("j_username").send_keys(user)
        driver.find_element_by_name("j_password").send_keys(pas)
        #driver.find_element_by_id("formSubmit").click()
        #Waits for next page to load
        while True:
            try:
                driver.find_element_by_name("_eventId_proceed").click()
                break
            except Exception as e:
                None
        print("Adding Courses to Task List...")
        #Keep track of the number of courses that were added, change and a counter
        numAdded = 0
        numChanged = 0
        i = 1
        #Waits for the page to load to find all the classes
        try:
            element_present = EC.presence_of_element_located((By.XPATH, "/html/body/form/div/main/div[1]/div/div/div[1]/nav/div/select/optgroup/option"))
            WebDriverWait(driver, timeout).until(element_present)
            classesTemp = driver.find_elements_by_xpath("/html/body/form/div/main/div[1]/div/div/div[1]/nav/div/select/optgroup/option")
        except TimeoutException:
            print("Timed out waiting for page to load.")
            time.sleep(2)
            main()
        #List of classes in webassign
        classes = []
        #Adds all classes to the list, otherwise the course.text object is deprecated on page change
        for course in classesTemp:
            classes.append(course.text)
        #Loops through all courses and scrapes the data and adds it to Google Taks
        for course in classes:
            try:
                #Finds the course selector dropdown and selects the current course
                select = Select(driver.find_element_by_id('courseSelect'))
                select.select_by_visible_text(course)
                #Gets the current class name, ignroing section and meeting days
                currentClass = course.split(",")[0]
                if currentClass == "PY 206" or currentClass == "PY 209":
                    continue
                #Clicks the "Go" button to navigate to the course's page
                driver.find_element_by_xpath('/html/body/form/div/main/div[1]/div/div/div[1]/nav/div/button').click()
                #Tries to find all assignments, if an exception occurs it is assumed there are no assignments and the program proceeds to the next class
                try:
                    assignmentList = driver.find_element_by_xpath("/html/body/form/div/main/div[6]/div[1]/div[1]/section/ul")
                    assignments = assignmentList.find_elements_by_tag_name("li")
                except Exception as e:
                    continue
                #For each assigment get the name and the due date and add it to Google Tasks
                for assignment in assignments:
                    #Tries to get the name and due date, if exception occurs it is assumed it is not an assignments
                    #This is necessary because some teachers (physics) put test seats in as assigments
                    try:
                        assignmentName = assignment.find_element_by_xpath("a/div/span").text
                        assignmentDue = assignment.find_element_by_xpath("a/div[3]").text
                    except Exception as e:
                        continue
                    #Gets the assigment due date
                    aTS = assignmentDue.split(", ")
                    #Gets the time that the assigment is due
                    aTHMS = aTS[3].split(" ")
                    #Create a datetime object to format the time for Google Tasks API
                    date_time_obj = datetime.datetime.strptime(aTS[1] + " " + aTS[2], '%b %d %Y')
                    #Formats the task name
                    titleC = currentClass + " - " + assignmentName
                    #Creates a new task to be added to the Google Tasks list
                    add = {
                        'title' : prefix + currentClass + " - " + assignmentName,
                        'notes' : 'Due @ ' + aTHMS[0] + aTHMS[1],
                        'due' : date_time_obj.isoformat() + '.000Z'
                    }
                    #Calls the API and gets a list of all the tasks on the list for searching
                    fullTasks = service.tasks().list(tasklist='@default', showCompleted=True, showHidden=True, maxResults=100).execute()
                    #To booleans to store if the value is found or it needs a date time change
                    found = False
                    dtChange = False
                    #Searches all tasks on the tasklist and sees if it exists or needs a datetime change
                    for task in fullTasks['items']:
                        if task['title'] == prefix + currentClass + " - " + assignmentName or task['title'] == currentClass + " - " + assignmentName:
                            if task['due'] != add['due']:
                                dtChange = True
                            else:
                                found = True
                            break
                    #If the task needs a datetime change we need to remove it and readd it
                    if dtChange:
                        for task in fullTasks['items']:
                            if task['title'] == add['title']:
                                service.tasks().delete(tasklist='@default', task=task['id']).execute()
                    #If it is found or the assignment is ignored, skip it
                    if found or ignore(assignmentName):
                        continue
                    #Otherwise call the API and add it to the task list
                    result = service.tasks().insert(tasklist='@default', body=add).execute()
                    #If result is nothing then it was not added correclty, otherwise print the information about the assignment
                    if not result:
                        print('Could not add')
                    else:
                        if dtChange:
                            print("Change Date/Time: " + currentClass + " - " + assignmentName)
                            numChanged = numChanged + 1
                        else:
                            print("Added: " + currentClass + " - " + assignmentName)
                            numAdded = numAdded + 1
                i = i + 1
            #If an exception occurs anywhere in execution, print the message and stop execution
            except Exception as e:
                print(e.getMessage())
                break
        #Prints the number of assignmets added and number of assignments changed
        print("Assignments Added: %i, Assignments Changed: %i" % (numAdded, numChanged))
        #Waits for the user to hit enter to return to the main page and close chrome
        input("Press enter to return to main page")
        #Exits chrome
        driver.quit()

    #Otherwise the input is not valid and the user is reprmpted
    else:
        print("Not valid input")
        time.sleep(1)
        main()
#================================END MAIN======================================#

#Method to check if the assignment needs to be ignored
#TODO: Implement a file with ignored assignments
def ignore(name):
    if(name == "Access to Calculus 1 (MA 141) Textbook Files"):
        return True
    return False

#Method to remove the auth file
def remove():
    confirm = input("Are you sure you want to remove the auth file? (YES/NO)")
    if confirm == "YES":
        try:
            os.remove('token.pickle')
            sys.exit()
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            sys.exit()
    else:
        return

if __name__ == '__main__':
    main()