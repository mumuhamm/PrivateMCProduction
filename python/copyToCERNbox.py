#!/usr/bin/env python
import os, re, commands
import json

pathRoot = "root://xrootd.unl.edu/"
cernboxPath = "root://eosuser.cern.ch//eos/user/a/akalinow/"

cis_endpoint = "gsiftp://se.cis.gov.pl:2811"

directories = [
    "//dpm/cis.gov.pl/home/cms/store/user/akalinow/OMTF/9_3_14_displaced_100to500_20",
    "//dpm/cis.gov.pl/home/cms/store/user/akalinow/OMTF/9_3_14_displaced_100to500_500",
    "//dpm/cis.gov.pl/home/cms/store/user/akalinow/OMTF/9_3_14_displaced_10to50_20",
    "//dpm/cis.gov.pl/home/cms/store/user/akalinow/OMTF/9_3_14_noSecondaries_v1",
]

destinationPath = "/Data/9_3_14_Displaced_v4/"
sourcePath = 

for aDir in directories:
    
    command = " gfal-ls "+aDir
    print(command)
    os.system(command)



