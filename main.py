from datetime import datetime
from datetime import time
from connect import *
from action import *
import time
import schedule
import os
import json

def configload():
    path = "./Configs/"
    result = []
    for file in os.listdir(path):
        if file.endswith("-Config.json"):
            file_path = f"{path}/{file}"
            with open (file_path, "rb") as infile:
                result.append(json.load(infile))
    runcheck(result)

def runcheck(config_list):
    for i in config_list:
        path = "./Runs/"
        client_config = i
        client_name = client_config['name']
        client_ttr = client_config['TTR']
        run_file_name = client_name + '-Run.json'
        run_file = f"{path}{run_file_name}"
        run_exist = os.path.isfile(run_file)
        if run_exist == True:
            print("Run log exists at: " + run_file)
            with open(run_file) as f:
                runlog = json.load(f)
            runstart = runlog['lastrunstart']
            runstart = datetime.strptime(runstart, '%Y-%m-%d %H:%M')
        else:
            print("Run log does not exist at: " + run_file + " - Creating it now.")
            data = {
                "lastrunstart": "2000-01-01 01:01",
                "lastrunfinish": "",
                "lastrunerror": ""
            }
            with open(run_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            with open(run_file) as f:
                runlog = json.load(f)
            runstart = runlog['lastrunstart']
            runstart = datetime.strptime(runstart, '%Y-%m-%d %H:%M')
            runerror = runlog['lastrunerror']
        isrunreq = runreq(client_ttr,runstart)
        if isrunreq == True:
            print('Client: '+ client_name + ' is outdated - Running now.')
            secrets = pullsecrets(client_name)           
            fin_files = action(client_config, secrets)

        else:
            print('Client: '+ client_name + ' is already current and does not need a run.')
        
def runreq(runtime,runstart):
    currenttime = datetime.now().strftime("%Y-%m-%d %H:%M")
    currenttime = datetime.strptime(currenttime, '%Y-%m-%d %H:%M')
    timediff =  currenttime - runstart
    minsdif = int(timediff.total_seconds() / 60)
    if minsdif < runtime:
        return False
    else:
        return True

def pullsecrets(target_name):
    secretsfile = "/mnt/secrets-store/autoklean-secrets"
    with open(secretsfile) as f:
        secrets = json.load(f)
    secretsjson = secrets[target_name]  
    return(secretsjson)
       

schedule.every(10).seconds.do(configload)

while True:
    schedule.run_pending()
    time.sleep(1)


