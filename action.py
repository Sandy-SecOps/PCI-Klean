from connect import connect
from Actions.decrypt import decrypt
from Actions.unpack import unpack
from Actions.pcifilter import pci_process

def action(client_config, secrets):
    
    target_files = []
    stage = 'pull'
    target_files = connect(client_config, stage, secrets, target_files)

    if not target_files:
        print(client_config['name'] + ' has no files stored - Exiting.')
        return
    
    print ('_____________________')
    print ('Starting files are:')
    print (target_files)
    print ('_____________________')
   
    target_files = decrypt(client_config, target_files)
    print ('_____________________')
    print ('Post decrypt files are:')
    print (target_files)
    print ('_____________________')
   
    target_files = unpack(target_files)
    print ('_____________________')
    print ('Post unpack files are:')
    print (target_files)
    print ('_____________________')
   
    target_files = pci_process(target_files)
    print ('_____________________')
    print ('Post PCI Obf files are:')
    print (target_files)
    print ('_____________________')


