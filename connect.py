from ConMethods.azureblob import azureblob_con
from ConMethods.https import https_con
from ConMethods.s3 import s3_con
from ConMethods.sftp import pullfile, pushfile

def connect(client_config, stage, secrets, target_files):
    client_conmethod = client_config['conmethod']
    client_name = client_config['name']
    if client_conmethod == "sftp":
        if stage == 'pull':
            local_file_list = pullfile(client_config, secrets)
            return (local_file_list)
        elif stage == 'push':
            pushfile(client_config,secrets,target_files)

    elif client_conmethod == "https":
        https_con()
    elif client_conmethod == "s3":
        s3_con()
    elif client_conmethod == "azureblob":
        azureblob_con()
    else:
        print('No connection method defined for: ' + client_name + ' in config.')