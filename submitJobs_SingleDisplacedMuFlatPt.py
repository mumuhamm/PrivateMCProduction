#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleDisplacedMuPt1to100Eta24Dxy0to100_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleDisplacedMuFlatPt"
eventsPerJob = 5000
numberOfJobs = 10
outLFNDirBase = "/store/user/akalinow/OMTF/"
storage_element="T2_PL_Swierk"
outputDatasetTag = "11_01_2023"
withPileUp = False
runLocal = True

turnOffG4Secondary = True

iPtTest = 0 
signTest = -1
etaRange = (-3,3)
dxyRange = (0,100)
#########################################
#########################################
for iPt in range(0,3):
    for sign in range(-1,1,2):

        if iPt!=iPtTest or sign!=signTest:
            continue  

        requestName = "DisplacedMu_ch"+str(sign+1)+"_iPt"+str(iPt)+"_"+outputDatasetTag

        process = runCMSDriver(era, withPileUp, generator_fragment)
        process = adaptGunParameters(process, iPt, sign, etaRange, turnOffG4Secondary, dxyRange=dxyRange)

        dumpProcess(process, "PSet.py")

        prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

        if not runLocal:
            os.system("crab submit -c crabTmp.py")
            os.system("rm -f PSet.py* crabTmp.py*")                  
########################################################
