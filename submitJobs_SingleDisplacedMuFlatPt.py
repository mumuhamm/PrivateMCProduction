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
outputDatasetTag = "20_06_2023_test"
withPileUp = False
withReco = False
runLocal = True

turnOffG4Secondary = True

iPtTest = None
signTest = None
etaRange = (-3,3)
##NOTE: displacement expressed in mm
dxyRange = (0,100)
LxyMax = 200
LzMax = 10
#########################################
#########################################
for iPt in range(0,3):
    for sign in range(-1,1,2):

        if iPtTest!=None and signTest!=None and (iPt!=iPtTest or sign!=signTest):
            continue 

        requestName = "DisplacedMu_ch"+str(sign+1)+"_iPt"+str(iPt)+"_"+outputDatasetTag

        process = runCMSDriver(era, withPileUp, withReco, generator_fragment)
        process = adaptGunParameters(process, iPt, sign, etaRange, turnOffG4Secondary, 
                                    dxyRange=dxyRange, LxyMax=LxyMax, LzMax=LzMax)

        dumpProcess(process, "PSet.py")

        prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

        if not runLocal:
            os.system("crab submit -c crabTmp.py")
            os.system("rm -f PSet.py* crabTmp.py*")                  
########################################################
