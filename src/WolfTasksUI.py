from CalendarAPI import getTasksFromCalendar

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