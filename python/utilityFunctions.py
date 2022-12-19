import os, math, glob
from termcolor import colored

import FWCore.ParameterSet.Config as cms

from crab3 import *
#########################################
#########################################
pileup_inputs = {
    "Run2029":" ",
    }
#########################################
#########################################
eras_conditions = {
    "Run2029":"--era Phase2C9  --conditions 123X_mcRun4_realistic_v3 --geometry Extended2026D49",
    }
#########################################
#########################################
def runCMSDriver(era, withPileUp, generator_fragment):
    
    premix_switches = "--step GEN,SIM,DIGI,L1,DIGI2RAW "
    if withPileUp:
         premix_switches = premix_switches.replace("DIGI","DIGI,DATAMIX")
         premix_switches += pileup_inputs[era]+" "
         premix_switches += "--procModifiers premix_stage2 --datamix PreMix "

    if era=="Run2029":
        premix_switches = premix_switches.replace("DIGI,L1","DIGI,L1TrackTrigger,L1")
        premix_switches += "--beamspot HLLHC14TeV "
        premix_switches += "--customise_commands 'process.VtxSmeared.BunchLengthInm = cms.double(0.035)' "
        premix_switches += "--customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000 "
        premix_switches += "--customise L1Trigger/Configuration/customisePhase2TTOn110.customisePhase2TTOn110 "
        premix_switches += "--customise Configuration/DataProcessing/Utils.addMonitoring "
        premix_switches += "--customise UserCode/OmtfAnalysis/privateCustomizations.customize_L1TkMuonsGmt "
        premix_switches += "--customise UserCode/OmtfAnalysis/privateCustomizations.customize_outputCommands "     

    command = "cmsDriver.py " 
    command += generator_fragment+" "
    command += "--processName fullsim " 
    command += "--fileout file:FEVTSIM.root " 
    command += "--mc --eventcontent FEVTSIM "
    command += premix_switches 
    command += eras_conditions[era] +" "
    command += "--nThreads 1 "
    command += "--python_filename PSet.py -n 2 --no_exec "    

    if generator_fragment.find("DoubleMu")==-1:
        command += "--customise SimG4Core/CustomPhysics/Exotica_HSCP_SIM_cfi.customise "

    print(colored("cmsDriver command:","blue"),command)
    os.system(command)
    from PSet import process
    return process
#########################################
#########################################
def adaptGunParameters(process, iPt,sign, turnOffG4Secondary):

    chargeNames = ["m", "p"]
    ##Set run number (will be the same for all jobs!)
    process.source.firstRun = cms.untracked.uint32(iPt)
    ##Set output file name (will be extended by Crab with a random string)
    fileName = str(iPt)+"_"+chargeNames[sign+1]
    process.FEVTSIMoutput.fileName =  cms.untracked.string('SingleMu'+"_"+fileName+'.root')
    ##Set kinematic ranges
    ptRanges = [0.,1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 6., 7., 8., 
                10., 12., 14., 16., 18., 20., 25., 30., 35., 40., 45., 
                50., 60., 70., 80., 90., 100., 120.0, 140.0, 1000.0]

    process.source.firstRun = cms.untracked.uint32(iPt)

    process.generator.PGunParameters.MinPt = cms.double(ptRanges[iPt-1])
    process.generator.PGunParameters.MaxPt = cms.double(ptRanges[iPt])
    process.generator.PGunParameters.MinOneOverPt = cms.double(1.0/100.0)
    process.generator.PGunParameters.MaxOneOverPt = cms.double(1.0/1.0)
    process.generator.PGunParameters.PartID = cms.vint32(-sign*13)
    process.generator.PGunParameters.MinPhi = cms.double(-math.pi)
    process.generator.PGunParameters.MaxPhi = cms.double(math.pi)
    process.generator.PGunParameters.MinEta = cms.double(-3.0)
    process.generator.PGunParameters.MaxEta = cms.double(3.0)
    process.generator.PGunParameters.AddAntiParticle = cms.bool(False)

    if turnOffG4Secondary:
        print(colored("Switching off secondaries in G4","red"))
        process.g4SimHits.StackingAction.KillDeltaRay = cms.bool(True)
        process.g4SimHits.StackingAction.KillGamma = cms.bool(True)
        process.g4SimHits.StackingAction.KillHeavy = cms.bool(True)
        process.g4SimHits.StackingAction.GammaThreshold = cms.double(1E9)
        process.g4SimHits.StackingAction.SaveAllPrimaryDecayProductsAndConversions = cms.untracked.bool(False)

    return process
#########################################
#########################################
def dumpProcess(process, fileName):

    out = open(fileName,'w')
    out.write(process.dumpPython())
    out.close()
#########################################
#########################################
def prepareCrabCfg(era,
                   eventsPerJob,
                   numberOfJobs,
                   outLFNDirBase,
                   storage_element,
                   requestName,
                   outputDatasetTag):
    
    outputPrimaryDataset = requestName
    print(colored("requestName:","blue"),requestName)          
    print(colored("outputPrimaryDataset:","blue"),outputPrimaryDataset)
    print(colored("outputDatasetTag:","blue"),outputDatasetTag)

    ##Modify CRAB3 configuration
    config.JobType.allowUndistributedCMSSW = True
    config.JobType.pluginName = 'PrivateMC'
    config.JobType.psetName = 'PSet.py'
    config.JobType.numCores = 1
    config.JobType.maxMemoryMB = 2500
    
    config.General.requestName = requestName
    config.General.workArea = "Tasks_"+era
    
    config.Data.inputDataset = None
    config.Data.outLFNDirBase = outLFNDirBase+outputDatasetTag
    config.Data.publication = True
    config.Data.outputPrimaryDataset = outputPrimaryDataset
    config.Data.outputDatasetTag = outputDatasetTag

    config.Site.storageSite = storage_element
    
    config.Data.unitsPerJob = eventsPerJob
    config.Data.totalUnits = eventsPerJob*numberOfJobs

    fullWorkDirName = config.General.workArea+"/crab_"+config.General.requestName
    requestExists = len(glob.glob(fullWorkDirName))!=0
    if requestExists:
        print(colored("Request with name: {} exists. Skipping.".format(fullWorkDirName), "red"))
        return

    out = open('crabTmp.py','w')
    out.write(config.pythonise_())
    out.close()    
#########################################
#########################################