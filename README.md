# PrivateMCProduction
Python scripts for running private Monte Carlo event production for the CMS experiment as the LHC.

## Installation instructions:

* setup the CMSSW_13_1_0 work area according to the L1PhaseII
  [TWiki](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TPhase2Instructions#Recipe_for_the_full_CMSSW_13_1_p)
 with GeneratorFragments add-ons:

```Shell
 
cd CMSSW_13_1_0/src/
cmsenv
git cms-init 
git cms-checkout-topic -u cms-l1t-offline:Phase2_prototypeSnapshot_3_CMSSW_13_1
git clone git@github.com:akalinow/usercode-OmtfAnalysis UserCode/ -b devel_AK
mkdir -p Configuration/GenProduction/
git clone git@github.com:cms-sw/genproductions.git Configuration/GenProduction
mv  Configuration/GenProduction/genfragments Configuration/GenProduction/python
rm -rf  Configuration/GenProduction/python/ThirteenTeV/DisappTrksAMSB/
rm -rf  Configuration/GenProduction/python/ThirteenTeV/DelayedJets/
rm -rf  Configuration/GenProduction/python/ThirteenTeV/DMSIMP_Extensions
rm -f   Configuration/GenProduction/python/EightTeV/Exotica_HSCP_SIM_cfi.py
scram b -j 4
```

* fetch this repository:

```Shell
git clone git@github.com:akalinow/PrivateMCProduction.git
cd PrivateMCProduction
```

## Run instructions

* the private generator fragment templates are stored in the [GenFragments](GenFragments) directory
* the details of the generator configuration are set in functions located in [python/utilityFunctions.py
](python/utilityFunctions.py) file

The jobs are submitted with command depending on the process to generate:

* single muons with flat pt spectrum in three bins: [1,10], [10,100], [100, 1000].
```Shell
./submitJobs_SingleMuFlatPt.py
```

* single muons with flat spectrum in 1/pt in range [1,100].
```Shell
./submitJobs_SingleMuOneOverPt.py
```

* exotic scansions: HSCP and displaced:

```Shell
submitJobs_SingleStauFlatPt.py
submitJobs_SingleStopFlatPt.py
submitJobs_SingleDisplacedMuFlatPt.py
```

The eta range is set in the submission script:
```Python
etaRange = (-2.5,2.5)
```

other kinematic parameters are assumed to be fixed, and are set dedicated functions defined in [python/utilityFunctions.py](python/utilityFunctions.py).