from CalendarAPI import *

def main():
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

    print("Would you like to [view], [add], or [remove] tasks? ")
    while 1:
        action = input().lower()
        if action == 'view':
            getTasks(getEvents(createCalendarURL("https://moodle-courses2021.wolfware.ncsu.edu/calendar/export_execute.php?userid=138996&authtoken=25051e72c7311e1a04bdf806ec0af99ffea47dcf&preset_what=all&preset_time=custom")), 1)
            print("VIEW")
        elif action == 'add':
            print("ADD")
        elif action == 'remove':
            print("REMOVE")
        elif action == 'exit' or action == 'quit':
            exit(0)
        else:
            print("INVALID")


  
if __name__ == '__main__':
    main()