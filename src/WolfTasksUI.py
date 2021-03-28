from CalendarAPI import getTasksFromCalendar
from TasksAPI import *
import time

def main(service):
    print("                      .")
    print("                     / V\\")
    print("                   / ` /")
    print("                  <<  |")
    print("                  /   |")
    print("                /     |")
    print("              /       |")
    print("             /        |")
    print("           /    \  \ /")
    print("          (      ) | |")
    print("  ________|   _/_  | |")
    print("<__________\______)\__)")
    print("===================================")
    print("|            WolfTasks            |")
    print("===================================")

    while 1:
        print("Would you like to [view], [add] tasks or exit? ")
        action = input().lower().strip()
        if action == 'view':
            task_list = view(service)
            print("Tasks: ")
            for task in task_list:
                print(" - " + task.title + " @ " + task.due)
        elif action == 'add':
            numtype = -1
            bcalurl = True
            while 1:
                print("Would you like to input a [file] or [url]?")
                calorurl = input().lower().strip()
                if calorurl == 'file':
                    bcalurl = False
                    break
                elif calorurl == 'url':
                    bcalurl = True
                    break
                else:
                    print("Invalid option")
            print("Please enter your file path or calendar url:")
            url = input()
            while 1:
                print("What style formatting would you like?")
                print("Style 0: 'LLL###:' or Style 1: '[LLL ###]'")
                styletype = input().lower().strip()
                if styletype == '1' or styletype == 'one':
                    numtype = 1
                    break
                elif styletype == '0' or styletype == 'zero':
                    numtype = 0
                    break
                else:
                    print("Invalid option")
            tasks = getTasksFromCalendar(bcalurl, url, numtype)
            addAllTasks(service, tasks)
        elif action == 'exit' or action == 'quit' or action == 'q' or action == 'e':
            exit(0)
        else:
            print("Invalid option.")
        
        time.sleep(3)
        print()


  
if __name__ == '__main__':
    service = checkAuth()
    main(service)