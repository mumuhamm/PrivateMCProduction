#!/bin/bash

## CREATE GEN CFG FILE #####
# cmsDriver command

#GEN
cmsDriver.py Configuration/GenProduction/python/Guns/DoublePi0Pt10To200_Eta0To1p4_genfragment_cfi.py --python_filename DoublePi0Pt10To200-RunIISummer20UL17-00960_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN --fileout file:DoublePi0Pt10To200-RunIISummer20UL17wmGEN-00960.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(315)" --step GEN --geometry DB:Extended --era Run2_2017 --no_exec --mc -n 100

###SIM

#cmsDriver.py  --python_filename DoublePi0Pt10To200-RunIISummer20UL17SIM-00227_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:DoublePi0Pt10To200-RunIISummer20UL17SIM-00227.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step SIM --geometry DB:Extended --filein file:DoublePi0Pt10To200-RunIISummer20UL17wmGEN-00960.root --era Run2_2017 --runUnscheduled --no_exec --mc -n 100

#cmsDriver.py  --python_filename DoublePi0Pt10To200-RunIISummer20UL17SIM-00227_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:DoublePi0Pt10To200-RunIISummer20UL17SIM-00227.root --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step SIM --geometry DB:Extended --filein file:DoublePi0Pt10To200-RunIISummer20UL17wmLHEGEN-00960.root --era Run2_2017 --runUnscheduled --no_exec --mc -n 100

### ADD PU PREMIX######

#cmsDriver.py  --python_filename DoublePi0Pt10To200-RunIISummer20UL17DIGIPremix-00227_1_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:DoublePi0Pt10To200-RunIISummer20UL17DIGIPremix-00227.root --pileup_input $(<pu_files_UL17_n100.txt) --conditions 106X_mc2017_realistic_v6 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:DoublePi0Pt10To200-RunIISummer20UL17SIM-00227.root --datamix PreMix --era Run2_2017 --runUnscheduled --no_exec --mc -n 100

##HLT Use 94X
#cmsDriver.py  --python_filename DoublePi0Pt10To200-RunIISummer20UL17HLT-00227_1_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:DoublePi0Pt10To200-RunIISummer20UL17HLT-00227.root --conditions 94X_mc2017_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2e34v40 --geometry DB:Extended --filein file:DoublePi0Pt10To200-RunIISummer20UL17DIGIPremix-00227.root --era Run2_2017 --no_exec --mc -n 100


##RECO AOD
#cmsDriver.py  --python_filename DoublePi0Pt10To200-RunIISummer20UL17RECO-00227_1_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:DoublePi0Pt10To200-RunIISummer20UL17RECO-00227.root --conditions 106X_mc2017_realistic_v6 --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --filein file:DoublePi0Pt10To200-RunIISummer20UL17HLT-00227.root --era Run2_2017 --runUnscheduled --no_exec --mc -n 100

##MINIAOD v2
#cmsDriver.py  --python_filename DoublePi0Pt10To200-RunIISummer20UL17MiniAODv2-00206_1_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:DoublePi0Pt10To200-RunIISummer20UL17MiniAODv2-00206.root --conditions 106X_mc2017_realistic_v9 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein file:DoublePi0Pt10To200-RunIISummer20UL17RECO-00227.root  --era Run2_2017 --runUnscheduled --no_exec --mc -n 100
