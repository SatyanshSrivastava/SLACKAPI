from pyclickup import ClickUp
from datetime import datetime
import json
import sys
import random
import requests


clickup = ClickUp("pk_*******") #Enter your own personal token

main_team = clickup.teams[0]
print(main_team)
main_space = main_team.spaces
#print(main_space.projects[0].get_all_tasks())
print(main_space[1].projects[0])

#The Following function tests the status of a task whether or not it was completed and the result is then utilised and sent to some other function.
def statusChecker(project): 
    for i in project.get_all_tasks():
        if i.due_date==None: pass
        elif (datetime.today())>(i.due_date):
            messageSenderToSlack("The task-->  <{name}> \n which was due for the date: {date} has not be completed and was assigned to \n{assignee}".format(name=i.name,date=i.due_date,assignee=i.assignees))
        elif ( (datetime.today()-i.due_date).days==1 ):
            messageSenderToSlack("The task-->  <{name}> \n is due for the date: {date} and the deadline is approaching for \n{assignee}".format(name=i.name,date=i.due_date,assignee=i.assignees))

#The following function sends message to slack according to the configuratino.
def messageSenderToSlack(messageClickup):
    url = "<ENTER WEBHOOK URL HERE>"
    message = messageClickup #this message is mapped to the variable
    title = (f"Task Updater :zap:")
    slack_data = {
        "username": "SATYANSH'S WORKSPACE",
        "icon_emoji": ":satellite:",
        "channel" : "general",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

testProject=main_team.spaces[0].projects[0] #Choosing the project space to look into
statusChecker(testProject) #Function call
