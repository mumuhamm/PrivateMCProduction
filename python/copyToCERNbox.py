#!/usr/bin/env python
import os, re, commands
import json

cernboxPath = "gsiftp://eosuserftp.cern.ch//eos/user/a/akalinow/" 
cis_endpoint = "gsiftp://se.cis.gov.pl:2811"

directories = [
    "//dpm/cis.gov.pl/home/cms/store/user/jwiechni/HSCP/Run2029_Marianna_14_12_2022/"    
]

destinationPath = "/Data/HSCP/"

for aDir in directories:
    theSource = cis_endpoint+aDir
    theDestination = cernboxPath + destinationPath
    command = "gfal-copy -r "+theSource+ " " + theDestination
    print(command)
    os.system(command)



