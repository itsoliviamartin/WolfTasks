# WolfTasks by 2B || !2B
> A tool that converts a class calendar of assignments (iCal) to Google Tasks.
> 
> This tool was originally developed for the Diamond Hacks hackathon at NCSU
> 
> Submission video: https://www.youtube.com/watch?v=1P5kbMaFMyk
>
> Email: <wolftasks.ncsu@gmail.com>
> 
> Devpost: https://devpost.com/software/wolftasks
<hr>

# Team Members
* Olivia Martin <itsoliviamartin@gmail.com> <ogmartin@ncsu.edu>
* Brooke Raschke <brookeraschke@gmail.com> <bmraschk@ncsu.edu>
* Zach Groseclose <zachgroseclose@gmail.com> <zmgrosec@ncsu.edu>

# Table of Contents
1) Usage
2) Future
<hr>

## Usage

### Dependencies
To use WolfTasks you will need python3 and a few python libraries (Install with PIP!)
* Python 3
* ICS
* google-api-python-client
* google-auth-httplib2 
* google-auth-oauthlib
* tkinter (for windows you will need to install manually. Download here: <https://www.activestate.com/products/python/downloads>)

### How to use
There are two different ways to use WolfTasks, the command line user interface and the graphical user interface.

Both options will first authenticate with a Google account which will be used for adding the tasks with.

To launch the command line UI:
1) Change directory to the src directory in WolfTasks
2) run **python WolfTasksUI.py**
3) The command line interface should run and prompt for input

To launch the GUI:
1) Change directory to the src directory in WolfTasks
2) run **python WolfTasksGUI.py**
3) The GUI will load and you can input the required fields via the radio buttons

## Future

There are a few things we hope to accomplish in the future. 
* Pack the python tool into one executable
* Created a website based tool that would allow users to upload the file or paste a link
