#!/usr/bin/env python3

import os

from utilityFunctions import *
#########################################
#########################################
CMSSW_BASE = os.environ.get("CMSSW_BASE")
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"

##Job steering parameters
generator_fragment=genFragmentsDirectory+"/"+"DoubleMuOneOverPt1to100Eta24_cfi.py"

era = "Run2029"
eventsPerJob = 100
numberOfJobs = 10
outLFNDirBase = "/store/user/akalinow/OMTF/"
storage_element="T2_PL_Swierk"
outputDatasetTag = "test_19_12_2022"
withPileUp = False
runLocal = True

turnOffG4Secondary = True

iPtTest = 16 
signTest = -1
#########################################
#########################################
for sign in range(-1,1,2):
    if iPt!=iPtTest or sign!=signTest:
        break  

    requestName = "SingleMu_ch"+str(sign+1)+"_OneOverPt"+"_"+outputDatasetTag

    process = runCMSDriver(era, withPileUp, generator_fragment)
    process = adaptGunParameters(process, iPt, sign, turnOffG4Secondary)
    dumpProcess(process, "PSet.py")

    prepareCrabCfg(era, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

    if not runLocal:
        os.system("crab submit -c crabTmp.py")
        os.system("rm -f PSet.py* crabTmp.py*")                
########################################################

