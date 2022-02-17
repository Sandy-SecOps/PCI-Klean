import re
import pandas as pd
from pathlib import Path
import time

def pci_process(target_files):
    
    for inputfile in target_files: 
        pf = Path(inputfile)
        f = str(pf.name)
        p = str(pf.parent)
        proc_files = []

        if pf.suffix == ('.csv'):
            print ('PCI Scanning: ' + inputfile)
            df = pd.read_csv(inputfile)
            obf_df = pci_stage1(df)
            obf_fn = (p + '/obf-'+ f)
            obf_df.to_csv(obf_fn, index=False)
            proc_files.append(obf_fn)
            print(inputfile)
            print(target_files)
            target_files.remove(inputfile)

        elif pf.suffix == ('.xls'):
            print ('PCI Scanning: ' + inputfile)
            df = pd.read_excel(inputfile)
            obf_df = pci_stage1(df)
            obf_fn = (p + '/obf-'+ f)
            obf_df.to_excel(obf_fn, index=False)
            proc_files.append(obf_fn)
            target_files.remove(inputfile)

        elif pf.suffix == ('.xlsx'):
            print ('PCI Scanning: ' + inputfile)
            df = pd.read_excel(inputfile, engine='openpyxl')
            obf_df = pci_stage1(df)
            obf_fn = (p + '/obf-'+ f)
            obf_df.to_excel(obf_fn, engine='openpyxl', index=False)
            proc_files.append(obf_fn)
            target_files.remove(inputfile)

        elif pf.suffix == ('.xml'):
            print ('PCI Scanning: ' + inputfile)
            df = pd.read_xml(inputfile)
            obf_df = pci_stage1(df)
            obf_fn = (p + '/obf-'+ f)
            obf_df.to_xml(obf_fn, index=False)
            proc_files.append(obf_fn)
            target_files.remove(inputfile)

        elif pf.suffix == ('.json'):
            print ('PCI Scanning: ' + inputfile)
            df = pd.read_json(inputfile)
            obf_df = pci_stage1(df)
            obf_fn = (p + '/obf-'+ f)
            obf_df.to_json(obf_fn, orient='split',index=False)
            proc_files.append(obf_fn)
            target_files.remove(inputfile)

        else:
            ext = pf.suffix
            print ('Unsupported file type, extension was: ' + ext)

    target_files.extend(proc_files)

    return (target_files)

def pci_stage1(df):
    startt= time.time()
    dfs = df.astype(str, copy=True, errors='raise').replace('\.0', '', regex=True)

    regexset = [
        r"(^3([347][0-9]{2})(?:[ -]?[0-9]{6})(?:[ -]?[0-9]{5})$)", #Amex
        r"(^4[0-9]{3}(?:[ -]?[0-9]{4}){3}$)", #Visa
        r"(^4[0-9]{3}(?:[ -]?[0-9]{4}){2}(?:[ -]?[0-9])$)", #Visa-Old 13 Digit
        r"(^(?:5[0-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)(?:[ -]?[0-9]{4}){3}$)", #Mastercard
        r"(^3(?:0[0-5][0-9]|[68][0-9][0-9])(?:[ -]?[0-9]{4}){2}(?:[ -]?[0-9]{2})$)", #Diner/Carte Blanche
        r"(^6(?:011|5[0-9]{2})(?:[ -]?[0-9]{4}){3}$)", #Discover
        r"(^(2131|1800|35[0-9]{2})(?:[ -]?[0-9]{4}){3}$)", #JCB
        r"(^(6541|6556)(?:[ -]?[0-9]{4}){3}$)",#BCGlobal

    ]

    for c in dfs.columns:
        dfs[c] = dfs[c].str.replace('|'.join(regexset),pci_obf)

    #HouseKeeping
    endt =time.time()
    print (f" Runtime was {endt - startt}")

    return (dfs)

def pci_obf(asset):
    ccnum = asset.group()
    ccnumtail = ccnum[-4:]
    ccnumtbo = ccnum[:-4]
    obfdata = re.sub(r'\d', 'X', ccnumtbo)
    obfdata = (obfdata + ccnumtail)
    return (obfdata)




