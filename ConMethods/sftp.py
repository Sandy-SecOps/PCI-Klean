import paramiko
import re
import pathlib

def pullfile(client_config, secrets):
    hostname = secrets['pull-hostname']
    username = secrets['pull-username']
    passwrd = secrets['pull-password']
    target_name = client_config['name']
    target_files=[]
    local_files_list=[]

    if client_config['is_name_conv'] == True:
        in_file = client_config['in_filename']
        in_file = in_file.format(**client_config)
        in_file = in_file.replace('.', '\.')
        in_file = in_file.replace('*','\w*' )
        in_file = re.compile(in_file)

    else:
        in_file = client_config['in_filename']

    in_path = client_config['in_filepath']

    ssh_client =paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname,username=username,password=passwrd)
    sftp = ssh_client.open_sftp()
    
    for filename in sftp.listdir(in_path):
        if re.match(in_file, filename):
            if not filename.endswith(('-WORKING','-COMPLETED')):
                # file_path = (in_path + filename)
                target_files.append(filename)
            else:
                print ('No live files needing to be processed for client: ' + target_name)

    remotepath = client_config['in_filepath']
    localpath = "/working/"+target_name+"/"
    path = pathlib.Path(localpath)
    path.mkdir(parents=True, exist_ok=True)

    for i in target_files:
        localfile = (localpath + i )
        remotefile = (remotepath + i)
        remote_working = (remotefile + '-WORKING')
        sftp.get(remotefile,localfile)
        # sftp.rename(remotefile, remotefile + '-WORKING') **REMOVE THIS FOR TESTING**
        local_files_list.append(localfile)
    return(local_files_list)


def pushfile(client_config, secrets,target_files):
    hostname = secrets['pull-hostname']
    username = secrets['pull-username']
    passwrd = secrets['pull-password']
    target_name = client_config['name']
    out_path = client_config['out_filepath']
    out_file = client_config['out_filename']

    ssh_client =paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname,username=username,password=passwrd)
    ssh_client.close()
    
    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, password=passwrd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    localpath = "/working/"+target_name+"/"




    
    
    