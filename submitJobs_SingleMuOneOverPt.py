#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleMuOneOverPt1to100Eta24_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleMuOneOverPt"
eventsPerJob = 100
numberOfJobs = 10
outLFNDirBase = "/store/user/akalinow/OMTF/"
storage_element="T2_PL_Swierk"
outputDatasetTag = "test_19_12_2022"
withPileUp = False
runLocal = True

turnOffG4Secondary = True

signTest = -1
etaRange = (-3,3)
#########################################
#########################################
for sign in range(-1,1,2):
    if sign!=signTest:
        continue  

    requestName = "SingleMu_ch"+str(sign+1)+"_OneOverPt"+"_"+outputDatasetTag

    process = runCMSDriver(era, withPileUp, generator_fragment)
    process = adaptGunParameters(process, -1, sign, etaRange, turnOffG4Secondary)
    dumpProcess(process, "PSet.py")

    prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

    if not runLocal:
        os.system("crab submit --dryrun -c crabTmp.py")
        os.system("rm -f PSet.py* crabTmp.py*")                
########################################################

