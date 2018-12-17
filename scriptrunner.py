import os
from subprocess import PIPE, run, call
import boto3

cmdDict={
    'python3':'python3 $(SCRIPT_NAME) $(ARGS)',
}
INSTANCE_ID = os.environ['INSTANCE_ID']
RESULT_BUCKET_NAME = os.environ['RESULT_BUCKET_NAME']
DATA_BUCKET_NAME = os.environ['DATA_BUCKET_NAME']

s3Resource = boto3.resource('s3')
bucket = s3Resource.Bucket(DATA_BUCKET_NAME)

try:
    RUNTIME = os.environ['RUNTIME']
    SCRIPT_NAME = os.environ['SCRIPT_NAME']
    
    taskList = [line.strip() for line in open("tasklist.txt", 'r')]
    if len(taskList)>0:
        taskListUpdated = [line.strip() for line in open("tasklist.txt", 'r')]
        with open('tasklist.txt', 'w') as f:
            for line in taskList[1:]:
                f.write(line+'\n')
        objFileName=taskList[0]
        bucket.download_file(objFileName, objFileName)
        command = cmdDict[RUNTIME]
        command = command.replace('$(SCRIPT_NAME)', SCRIPT_NAME)
        command = command.replace('$(ARGS)', objFileName)
        call(command, shell=True)
        s3Resource.Bucket(RESULT_BUCKET_NAME).upload_file(objFileName, objFileName+'_by_'+INSTANCE_ID)
        objAcl = s3Resource.ObjectAcl(RESULT_BUCKET_NAME,objFileName+'_by_'+INSTANCE_ID)
        objAcl.put(ACL='public-read')
except:
    pass




