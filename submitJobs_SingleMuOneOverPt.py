#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleMuOneOverPt1to100Eta24_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleMuOneOverPt"
eventsPerJob = 5000
numberOfJobs = 200
outLFNDirBase = "/store/user/akalinow/Data/SingleMu/"
#storage_element="T2_PL_Swierk"
storage_element="T3_CH_CERNBOX"
outputDatasetTag = "12_5_2_p1_22_02_2023"
withPileUp = False
withReco = False
runLocal = False

turnOffG4Secondary = False

signTest = None
etaRange = (-2.5,2.5)
#########################################
#########################################
for sign in range(-1,3,2):

    if signTest!=None and sign!=signTest:
        continue  

    requestName = "SingleMu_ch"+str(sign+1)+"_OneOverPt"+"_"+outputDatasetTag

    process = runCMSDriver(era, withPileUp, withReco, generator_fragment)
    process = adaptGunParameters(process, -1, sign, etaRange, turnOffG4Secondary)
    dumpProcess(process, "PSet.py")

    prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

    if not runLocal:
        os.system("crab submit -c crabTmp.py")
        os.system("rm -f PSet.py* crabTmp.py*")                
########################################################

