#!/usr/bin/env python3

import os

from utilityFunctions import *
#########################################
#########################################
CMSSW_BASE = os.environ.get("CMSSW_BASE")
genFragmentsDirectory = "Configuration/GenProduction/python/ThirteenTeV/HSCP/"

generator_fragments = [
                       "HSCPstop_M_800_TuneCP5_13TeV_pythia8_cff.py",
                       #"HSCPppstau_M_200_TuneZ2star_13TeV_pythia6_cff.py",
                       #"HSCPppstau_M_432_TuneZ2star_13TeV_pythia6_cff.py"                       
                       ]

##Job steering parameters
era = "Run2029"
eventsPerJob = 100
numberOfJobs = 10
outLFNDirBase = "/store/user/akalinow/HSCP/"
storage_element="T2_PL_Swierk"
outputDatasetTag = "test_19_12_2022"
withPileUp = False
runLocal = True
#########################################
#########################################
for aGenFragment in generator_fragments:

    requestName = aGenFragment.split("cff")[0].rstrip("_")
    requestName+="_"+outputDatasetTag
    process = runCMSDriver(era, withPileUp, genFragmentsDirectory+aGenFragment)
    dumpProcess(process, "PSet.py")

    prepareCrabCfg(era, eventsPerJob, numberOfJobs,
                  outLFNDirBase, storage_element, 
                  requestName, outputDatasetTag)

    if not runLocal:
        os.system("crab submit -c crabTmp.py")
        os.system("rm -f PSet.py* crabTmp.py*")                
########################################################

