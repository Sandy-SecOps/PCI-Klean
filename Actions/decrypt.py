import gnupg

def decrypt(client_config, target_files):

    encfiles =[]

    for x in target_files:
        if x.endswith('.pgp'):
            encfiles.append(x)
        else:
             print (x + ' does not have a pgp extension.')

    if encfiles:
        target_files = [x for x in target_files if x not in encfiles]
        decrypted_files = decrypt_action(client_config, encfiles)
        target_files.extend(decrypted_files)
        return(target_files)
    else:
        print ('There was no encrypted files. Returning.')
        return(target_files)


def decrypt_action(client_config, target_files):

    if client_config['enc_type'] == 'pgp' and client_config['uses_cert_enc']:
        decrypted_files = []
        name = client_config['name']
        env = client_config['env']
        cert = ("/mnt/secrets-store/"+name+"-"+env+"-private")
        gpg = gnupg.GPG(gnupghome='/root')
        with open (cert) as cert:
            cert_data = cert.read()
        import_result = gpg.import_keys(cert_data)
        # for key in import_result.results:
        #     print(key)
        for i in target_files:
            if i.endswith('pgp'):
                outputfilename = i.replace('.pgp','')
                with open (i, 'rb') as inputfile:
                    status = gpg.decrypt_file(file=inputfile, output=outputfilename)
                dec_status = status.status
                print ( i + ' - status: ' + dec_status)
                decrypted_files.append(outputfilename)
    return(decrypted_files)
