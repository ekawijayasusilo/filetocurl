import os
from subprocess import PIPE, run, call
import boto3

cmdDict={
    'python3':'python3 $(SCRIPT_NAME) $(ARGS)',
}
RUNTIME = os.environ['RUNTIME']
SCRIPT_NAME = os.environ['SCRIPT_NAME']

taskList = [line.strip() for line in open("tasklist.txt", 'r')]
if len(taskList)>0:
    command = cmdDict[RUNTIME]
    command = command.replace('$(SCRIPT_NAME)', SCRIPT_NAME)
    command = command.replace('$(ARGS)', taskList[0])
    call(command, shell=True)
    taskList = [line.strip() for line in open("tasklist.txt", 'r')]
    with open('tasklist.txt', 'w') as f:
        for line in taskList[1:]:
            f.write(line+'\n')

