#!/usr/bin/env python3

import os

from utilityFunctions import *
#########################################
#########################################
CMSSW_BASE = os.environ.get("CMSSW_BASE")
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"

##Job steering parameters
generator_fragment=genFragmentsDirectory+"/"+"DoubleMuPt1to100Eta24_cfi.py"
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
iPtMin = 1
iPtMax = 32

iPt = 16 #TEST
sign = -1
#########################################
#########################################
requestName = "SingleMu_ch"+str(sign+1)+"_iPt"+str(iPt)+"_"+outputDatasetTag
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

